#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 22:28:48 2017

@author: ruobingwang
"""
from spacy.en import English
from gat.service import file_io
import spacy
import pandas as pd
from nltk import data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datefinder
import re
import textacy
import datetime
from dateparser import parse
import time
from nltk.stem import WordNetLemmatizer
import numpy as np
from gat.dao import dao


class SVOSENT(object):
    """
    Class Methods to Extract Subject Verb Object Tuples and sentiments from a Sentence
    """

    def __init__(self, language='english'):
        """
        Initialize 
        """
        self.nlp = dao.spacy_load_en()
        self.sent_detector = data.load('tokenizers/punkt/english.pickle')
        self.analyzer = SentimentIntensityAnalyzer()  # for sentiment analysis
        self.keyverbs = list(pd.read_csv('KeyVerbs.csv')['key_verbs'])
        self.allcities = list(pd.read_csv('Allcities.csv')['City'])
        # self.emolexdict=pd.read_csv('emolex_full.csv')

    def getTexts(self, directory):
        # function by Tye
        # Input: Directory
        # Output:List of all text files in the directory fully loaded into memory
        texts = []
        pathnames = file_io.getFilesRecurse(directory, '.txt')
        for pathname in pathnames:
            texts.append(file_io.openFile(pathname))
        return texts

    def split_and_clean(self, text):
        '''
        Temporay function only useful for corpus data
        '''
        textlist = text.split('______________________________________________________')
        result = [text[text.find("Title:") + 6:text.find("Publication title")] for text in textlist if len(text) != 0]
        return result

    def get_svo(self, sentence):
        '''
        get SVO of single sentence
        '''
        parsed_phrase = self.nlp(sentence)
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
            if e.label_ == 'GPE' or e.label == 'LOC' or e.label_ == 'PERSON' or e.label_ == 'ORG' or e.label == 'NORP' or e.label == 'FACILITY' or e.label == 'PRODUCT':
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
            if text.pos_ == "VERB" and text.lemma_ in self.keyverbs:
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

    def get_svo_from_article(self, article):
        sentences = self.sentence_split(article)
        val = []
        for sent in sentences:
            svoresult = self.get_svo(sent)
            val.append(svoresult)
        return pd.DataFrame(val)

    def sentence_split(self, text):
        sentences = self.sent_detector.tokenize(text)
        return sentences

    def sentimentAnalysis(self, sentence):
        result = self.analyzer.polarity_scores(sentence)
        result['Sentence'] = sentence
        return result

    def get_senti_from_article(self, article):
        sentences = self.sentence_split(article)
        val = []
        for sent in sentences:
            result = self.sentimentAnalysis(sent)
            val.append(result)
        return pd.DataFrame(val)

    ###############################################
    # get both SVO and sent in one dataframe


    def svo_senti_from_article(self, article, subject=None):
        title = article[0:article.find('(title_end)')]
        try:
            date = list(datefinder.find_dates(article))[-1]
        except:
            date = None
        sentences = self.sentence_split(article)
        val1 = []
        val2 = []

        for sent in sentences:
            val1.append(self.sentimentAnalysis(sent))
            val2.append(self.get_svo(sent))
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
            if eventdate == None:
                return None
            if articledate == None:
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
        if subject == None:
            return result
        else:
            return result[result['Names'].apply(lambda x: subject in x)]

    def WriteCSV(self, df, name):
        df.to_csv(name + '.csv', index=False)

    def batchProcessArticles(self, articles):  # articles are list of strings, can be got from split and clean
        t0 = time.time()
        results = []
        for i, article in enumerate(articles):

            try:
                result = self.svo_senti_from_article(article)
                results.append(result)
                print(i + 1, 'th/', len(articles), 'article is done')

            except Exception as e:
                print(i, 'th article has error:', e)

        t1 = time.time()
        results = pd.concat(results, axis=0)
        result = result.drop_duplicates(subset=['Sentence'], keep='first')  # remove duplicate rows
        print('time cost', end=':')
        print(t1 - t0)
        return results


if __name__ == "__main__":
    svo_sent = SVOSENT()

    article = '''
    North Korea threatens to attack South Korea on September 24th. United States and South Korea will have a meeting at Beijing. 
    '''
    result = svo_sent.svo_senti_from_article(article)
    print(result)
    '''
    articles_not=svo_sent.getTexts('corpus4')[-1]
    articles=svo_sent.split_and_clean(articles_not)
    import time
    t0=time.time()
    results=[]
    for i,article in enumerate(articles):
        try:
            result=svo_sent.svo_senti_from_article(article)
            results.append(result)
            print(i,end='th/')
            print(len(articles),end='')
            print(' article is done')
        except:
            print(i,' th article is empty!')
    #result2=svo_sent.svo_senti_from_article(article,'Robin')
    t1=time.time()
    results=pd.concat(results, axis=0)
    print('time cost',end=':')
    print(t1-t0)
    #print(results)
    svo_sent.WriteCSV(results,'corpus4_full_dataset')
    '''
