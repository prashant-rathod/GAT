import os
import math
import threading
import spacy
import time
import datefinder
import pandas as pd
from newspaper import Article
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from gat.service.SmartSearch.SEARCH_BING_MODULE import bingURL
from gat.service import file_io
from nltk import data
from dateparser import parse
from gat.dao import dao


class SmartSearchThread(threading.Thread):
    def __init__(self, language='english', search_question='', article_count=0):
        super().__init__()
        self.messages = []
        self.messages_lock = threading.Lock()
        self.result = None
        self.result_lock = threading.Lock()
        self.result_ontology = None
        self.result_ontology_lock = threading.Lock()
        self._nlp = dao.spacy_load_en()
        self.__sent_detector = data.load('tokenizers/punkt/english.pickle')
        self.__analyzer = SentimentIntensityAnalyzer()  # for sentiment analysis
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        self.__keyverbs = list(pd.read_csv(os.path.join(current_file_path, 'KeyVerbs.csv'))['key_verbs'])
        self.__allcities = list(pd.read_csv(os.path.join(current_file_path, 'Allcities.csv'))['City'])
        self.__search_question = search_question
        self.__article_count = int(article_count)

    @classmethod
    def __getTexts(cls, directory):
        # function by Tye
        # Input: Directory
        # Output:List of all text files in the directory fully loaded into memory
        texts = []
        pathnames = file_io.getFilesRecurse(directory, '.txt')
        for pathname in pathnames:
            texts.append(file_io.openFile(pathname))
        return texts

    @classmethod
    def __split_and_clean(cls, text):
        '''
        Temporay function only useful for corpus data
        '''
        textlist = text.split('______________________________________________________')
        result = [text[text.find("Title:") + 6:text.find("Publication title")] for text in textlist if len(text) != 0]
        return result

    def __get_svo(self, sentence):
        '''
        get SVO of single sentence
        '''
        parsed_phrase = self.__nlp(sentence)
        names = list(parsed_phrase.ents)
        corrected_names = []
        persons = []
        locations = []
        organizations = []
        event_date = []
        norp = []
        facilities = []
        events = []
        cities = []
        for e in names:
            if e.label_ == 'GPE' or e.label == 'LOC' or e.label_ == 'PERSON' or e.label_ == 'ORG' or e.label == 'NORP' \
                    or e.label == 'FACILITY' or e.label == 'PRODUCT':
                corrected_names.append(e.text)
            if e.label_ == 'GPE' or e.label == 'LOC':
                locations.append(e.text)
            # if e.text.lower() in self.allcities:   # detect cities, slowdone the speed
            #                    cities.append(e.text)
            if e.label_ == 'PERSON':
                persons.append(e.text)
            if e.label_ == 'ORG':
                organizations.append(e.text)
            if e.label == 'NORP':
                norp.append(e.text)
            if e.label == 'FACILITY' or e.label == 'PRODUCT':
                facilities.append(e.text)
            if e.label == 'EVENT':
                events.append(e.text)

        subjects = []
        objects = []
        verbs = []
        for text in parsed_phrase:
            if text.dep_.startswith("nsubj") or text.dep_ in ['conj']:
                subject = text.orth_
                subjects.append(subject)
            if text.dep_ in ["dobj", 'pobj', 'iobj']:
                object_ = text.orth_
                objects.append(object_)
            if text.pos_ == "VERB" and text.lemma_ in self.__keyverbs:
                verb = text.lemma_
                verbs.append(verb)

        # event date
        try:
            event_date = list(set(sentence.replace('.', '').split()) & {'Monday', 'Tuesday', 'Wednesday', 'Tursday',
                                                                        'Friday', 'Saturday', 'Sunday', 'Today',
                                                                        'today', 'Tomorrow', 'tomorrow', 'Yesterday',
                                                                        'yesterday'})[0]

        except:
            try:
                event_date = list(datefinder.find_dates(sentence))[0]
                if str(event_date.year) not in sentence:
                    event_date = str(event_date.month) + '/' + str(event_date.day)
                event_date = str(event_date)
            except:
                event_date = None

        # correct subject and object
        corrected_subjects = []
        corrected_objects = []
        corrected_names_copy = list(corrected_names)
        for sub in subjects:
            for name in corrected_names_copy:
                if sub in name:
                    corrected_subjects.append(name)
                    corrected_names_copy.remove(name)
                    break;
        for obj in objects:
            for name in corrected_names_copy:
                if obj in name:
                    corrected_objects.append(name)
                    corrected_names_copy.remove(name)
                    break;

        return {'Sentence': sentence,
                'Subjects': corrected_subjects,
                'Predicates': verbs,
                'Objects': corrected_objects,
                'Names': corrected_names,
                'Event_date': event_date,
                'Persons': persons,
                'Locations': locations,
                # 'Cities': cities,
                'Organizations': organizations,
                'NORP': norp,
                'Facilities': facilities,
                'Events': events}

    def __get_svo_from_article(self, article):
        sentences = self.__sentence_split(article)
        val = []
        for sent in sentences:
            svoresult = self.__get_svo(sent)
            val.append(svoresult)
        return pd.DataFrame(val)

    def __sentence_split(self, text):
        sentences = self.__sent_detector.tokenize(text)
        return sentences

    def __sentimentAnalysis(self, sentence):
        result = self.__analyzer.polarity_scores(sentence)
        result['Sentence'] = sentence
        return result

    def __get_senti_from_article(self, article):
        sentences = self.__sentence_split(article)
        val = []
        for sent in sentences:
            result = self.__sentimentAnalysis(sent)
            val.append(result)
        return pd.DataFrame(val)

    ###############################################
    # get both SVO and sent in one dataframe
    def __svo_senti_from_article(self, article, subject=None):
        title = article[0:article.find('(title_end)')]
        try:
            date = list(datefinder.find_dates(article))[-1]
        except:
            date = None
        sentences = self.__sentence_split(article)
        val1 = []
        val2 = []

        for sent in sentences:
            val1.append(self.__sentimentAnalysis(sent))
            val2.append(self.__get_svo(sent))
        result = pd.merge(pd.DataFrame(val1), pd.DataFrame(val2), on='Sentence')[
            ['Sentence', 'Names', 'Persons', 'Organizations', 'Facilities', 'Locations', 'Subjects', 'Predicates',
             'Objects', 'compound', 'Event_date']]
        result.rename(columns={'compound': 'Sentiment'}, inplace=True)
        #        try:
        #            result['date']=date
        #        except:
        #            result['date']='-----'
        result['Article_date'] = date
        result['Article_title'] = title

        def correctdate(eventdate, articledate):
            if eventdate is None:
                return None
            if articledate is None:
                return None
            try:
                corrected_date = parse(eventdate, settings={'RELATIVE_BASE': articledate})
            except:
                corrected_date = None
            return corrected_date

        result['Event_date'] = result['Event_date'].apply(lambda x: correctdate(x, date))
        #        try:
        #            result.loc[result['date']> datetime.datetime.today() + datetime.timedelta(days=1),'date']='-----'
        #        except:
        #            pass
        result = result.drop_duplicates(subset=['Sentence'], keep='first')  # remove duplicate rows
        '''
        ###emolex start
        def getEmolex(word):
            wordlist=re.findall(r'\w+', word)
            wordlist=[e.lower() for e in wordlist]
            df=pd.DataFrame(columns=list(self.emolexdict['type'].unique()))

            dflist=[]
            for e in wordlist:

                temp=self.emolexdict[self.emolexdict['word']==e]
                pivot=temp.pivot(index='word', columns='type', values='Weight').reset_index()
                dflist.append(pivot)
            result=pd.concat(dflist)
            features=list(result)
            features.remove('word')
            df[features]=result[features]
            df['Sentence']=word

            final=df.groupby('Sentence').apply(np.mean).reset_index()
            return final

        emolex_all=[]
        for sent in result['Sentence']:
            dft=getEmolex(sent)
            emolex_all.append(dft)

        result_emolex=pd.concat(emolex_all)
        result=result.join(result_emolex.set_index('Sentence'),on='Sentence')
        ###emolex end
        '''
        if subject is None:
            return result
        else:
            return result[result['Names'].apply(lambda x: subject in x)]

    @classmethod
    def __WriteCSV(cls, df, name):
        df.to_csv(name + '.csv', index=False)

    def __batchProcessArticles(self, articles):  # articles are list of strings, can be got from split and clean
        t0 = time.time()
        results = []
        for i, article in enumerate(articles):

            try:
                result = self.__svo_senti_from_article(article)
                results.append(result)
                self.messages_lock.acquire()
                self.messages.append(str(i + 1) + 'th/' + str(len(articles)) + 'article is done')
                self.messages_lock.release()

            except Exception as e:
                self.messages_lock.acquire()
                self.messages.append(str(i) + 'th article has error:' + str(e))
                self.messages_lock.release()

        t1 = time.time()
        results = pd.concat(results, axis=0)
        result = result.drop_duplicates(subset=['Sentence'], keep='first')  # remove duplicate rows
        self.messages_lock.acquire()
        self.messages.append('time cost' + ':')
        self.messages.append(str(t1 - t0))
        self.messages_lock.release()
        return results

    def __url_reader(self, url):
        article = Article(url)
        article.download()
        article.parse()
        title = article.title
        authors = article.authors
        date = article.publish_date
        text = article.text
        # can also include things like article images, and attached videos
        # article.nlp()
        # keywords = article.keywords
        # summary = article.summary
        self.messages_lock.acquire()
        self.messages.append("The article: {} is downloaded and parsed".format(title))
        self.messages_lock.release()
        return title, authors, date, text  # keywords , summary

    @classmethod
    def __to_string(cls, title, authors, date, text):  # mimic corpus style
        article = 'Title:' + title + '(title_end)' + 'Full text:' + text + 'Publication date - ' + str(
            date) + '____________________________________________________________'
        return article

    def __scrape_from_urls(self, urls):  # urls is list of string, each string is a url
        articles = ''
        t0 = time.time()
        for url in urls:
            try:
                title, authors, date, text = self.__url_reader(url)
                articles += self.__to_string(title, authors, date, text)
            except:
                self.messages_lock.acquire()
                self.messages.append('download failed')
                self.messages_lock.release()
        t1 = time.time()
        self.messages_lock.acquire()
        self.messages.append('cost time:' + str(t1 - t0))
        self.messages_lock.release()
        return articles

    def __generate_ontology(self, result):
        result['Audience'] = (
            result['Names'].apply(lambda x: set(x)) - result['Subjects'].apply(lambda x: set(x)) - result[
                'Objects'].apply(
                lambda x: set(x))).apply(lambda x: list(x))
        subjects = list(result['Subjects'])
        objects = list(result['Objects'])
        sentiment = list(result['Sentiment'])
        audiences = list(result['Audience'])
        all_combination1 = []
        for i in range(len(result)):
            if len(subjects[i]) != 0 and len(objects[i]) != 0:
                combine = []
                for x in range(len(subjects[i])):
                    for y in range(len(objects[i])):
                        combine.append([subjects[i][x], objects[i][y]])
                all_combination1.append(combine)

        dflist1 = []
        for i in range(len(all_combination1)):
            df = pd.DataFrame(all_combination1[i], columns=['Name', 'Agent'])
            df['sentiment'] = sentiment[i]
            dflist1.append(df)
        Name_Agent_pro = pd.concat(dflist1)

        Name_Agent_pro = Name_Agent_pro.groupby(['Name', 'Agent']).agg({'sentiment': 'mean'
                                                                        }).reset_index()

        Name_Agent = Name_Agent_pro.groupby('Name')['Agent'].apply(lambda x: pd.Series(x.values)).unstack()
        Name_Agent = Name_Agent.rename(columns={i: 'Agent_N{}'.format(i + 1) for i in range(len(Name_Agent))}).iloc[:,
                     0:10].reset_index()
        Name_Weight = Name_Agent_pro.groupby('Name')['sentiment'].apply(lambda x: pd.Series(x.values)).unstack()
        Name_Weight = Name_Weight.rename(columns={i: 'Agent_W{}'.format(i + 1) for i in range(len(Name_Weight))}).iloc[
                      :, 0:10].reset_index()
        labels = []

        for i in range(len(list(Name_Agent))):
            labels.append(list(Name_Agent)[i])
            labels.append(list(Name_Weight)[i])
        labels.remove('Name')
        Name_Agent_Weight = Name_Agent.merge(Name_Weight, on='Name')[labels]

        all_combination2 = []
        for i in range(len(result)):
            if len(subjects[i]) != 0 and len(audiences[i]) != 0:
                combine = []
                for x in range(len(subjects[i])):
                    for y in range(len(audiences[i])):
                        combine.append([subjects[i][x], audiences[i][y]])
                all_combination2.append(combine)

        dflist2 = []
        for i in range(len(all_combination2)):
            df = pd.DataFrame(all_combination2[i], columns=['Name', 'Audience'])
            df['sentiment'] = sentiment[i]
            dflist2.append(df)
        Name_Audience_pro = pd.concat(dflist2)

        Name_Audience_pro = Name_Audience_pro.groupby(['Name', 'Audience']).agg({'sentiment': 'mean'
                                                                                 }).reset_index()

        Name_Audience = Name_Audience_pro.groupby('Name')['Audience'].apply(lambda x: pd.Series(x.values)).unstack()
        Name_Audience = Name_Audience.rename(
            columns={i: 'Audience_N{}'.format(i + 1) for i in range(len(Name_Audience))}).iloc[:, 0:10].reset_index()
        Name_Weight_Audience = Name_Audience_pro.groupby('Name')['sentiment'].apply(
            lambda x: pd.Series(x.values)).unstack()
        Name_Weight_Audience = Name_Weight_Audience.rename(
            columns={i: 'Audience_W{}'.format(i + 1) for i in range(len(Name_Weight_Audience))}).iloc[:,
                               0:10].reset_index()
        labels = []

        for i in range(len(list(Name_Audience))):
            labels.append(list(Name_Audience)[i])
            labels.append(list(Name_Weight_Audience)[i])
        labels.remove('Name')
        Name_Audience_Weight = Name_Audience.merge(Name_Weight_Audience, on='Name')[labels]
        ontology = Name_Agent_Weight.merge(Name_Audience_Weight, on='Name', how='outer')
        ontology = ontology.drop_duplicates()
        ontology.columns = ['Name', 'Agent', 'W', 'Agent', 'W', 'Agent', 'W', 'Agent', 'W', 'Agent', 'W', 'Agent', 'W',
                            'Agent', 'W', 'Agent', 'W', 'Agent', 'W', 'Agent', 'W',
                            'Audience', 'W', 'Audience', 'W', 'Audience', 'W', 'Audience', 'W', 'Audience', 'W',
                            'Audience', 'W', 'Audience', 'W', 'Audience', 'W', 'Audience', 'W', 'Audience', 'W']
        return ontology

    def run(self):
        if self.__search_question:
            self.messages_lock.acquire()
            self.messages.append('Smart Search started.')
            self.messages_lock.release()
            bing = bingURL()
            t0 = time.time()
            urls = bing.search_urls(self.__search_question, math.ceil(self.__article_count / 20.0))
            t1 = time.time()
            self.messages_lock.acquire()
            self.messages.append('time cost:' + str(t1 - t0))
            self.messages.append('#urls found:' + str(len(urls)))
            self.messages_lock.release()
            articles = self.__scrape_from_urls(urls)
            articles_list = self.__split_and_clean(articles)
            self.result_lock.acquire()
            self.result = self.__batchProcessArticles(articles_list)
            self.result_lock.release()
            self.result_lock.acquire()
            self.result_ontology_lock.acquire()
            self.result_ontology = self.__generate_ontology(self.result)
            self.result_ontology_lock.release()
            self.result_lock.release()
