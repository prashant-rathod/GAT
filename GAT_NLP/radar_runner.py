############################## IMPORTS ##############################

# download stopwords
import os
import nltk
import random

download_path = "nltk_downloads/"
nltk.data.path.append(download_path)
nltk.download('stopwords', download_dir=download_path)
nltk.download('vader_lexicon', download_dir = download_path)
nltk.download('averaged_perceptron_tagger', download_dir = download_path)
nltk.download('wordnet', download_dir = download_path)

import string
from GAT_NLP.radar import graph
from operator import itemgetter
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.collocations import BigramAssocMeasures, TrigramAssocMeasures
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics.association import QuadgramAssocMeasures
from nltk import QuadgramCollocationFinder


############################## CONSTANTS ##############################

alph = list(string.ascii_lowercase)
bad_pos_list = ['CC', 'CD', 'DT', 'EX', 'IN', 'MD', 'PDT', 'PRP', 'PRP$', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB','SYM', 'RP', 'JJ','JJR','JJS']
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
bigram_measures = BigramAssocMeasures()
trigram_measures = TrigramAssocMeasures()
quadgram_measures = QuadgramAssocMeasures()
emotions = ['positive', 'negative', 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
optimum = [1, 1, 1, 1, 1, 1, 1, 1]
lexicon = {}

############################## FILE INPUT ##############################

# opens a file
def openFile(pathname):
    f = open(pathname, 'r', encoding='cp437')
    try:
        raw = f.read()
    except UnicodeDecodeError:
        print('UnicodeDecodeError: ' + pathname)
        return ''
    return raw

# finds all txt files in the inputted directory and returns a list of their locations
def getFiles(path):
    pathnames = []
    file_list = os.listdir(path)
    for i in range(len(file_list)):
        if file_list[i][-4:] == '.txt':
            pathnames.append(os.path.join(path, file_list[i]))
    return pathnames

# finds all txt files in the inputted directory and returns a list of their locations (recurse one level)
def getFilesRecurse(path):
    pathnames = []
    file_list = os.listdir(path)
    for i in range(len(file_list)):
        if file_list[i][-4:] == '.txt':
            pathnames.append(os.path.join(path, file_list[i]))
        elif os.path.isdir(path + '/' + file_list[i]):
            pathnames += getFiles(path + '/' + file_list[i])
    return pathnames

# reads lexicon from txt file
def readLexicon():
    f = open('static/lexicon.txt', 'r')
    raw = f.read().split('\n')
    for n in range(0, len(raw), 10):
        word = raw[n].split('\t')[0]
        lexicon[word] = []
        lexicon[word].append(int(raw[n+6].split('\t')[2])) # positive
        lexicon[word].append(int(raw[n+5].split('\t')[2])) # negative
        lexicon[word].append(int(raw[n+0].split('\t')[2])) # anger
        lexicon[word].append(int(raw[n+1].split('\t')[2])) # anticipation
        lexicon[word].append(int(raw[n+2].split('\t')[2])) # disgust
        lexicon[word].append(int(raw[n+3].split('\t')[2])) # fear
        lexicon[word].append(int(raw[n+4].split('\t')[2])) # joy
        lexicon[word].append(int(raw[n+7].split('\t')[2])) # sadness
        lexicon[word].append(int(raw[n+8].split('\t')[2])) # surprise
        lexicon[word].append(int(raw[n+9].split('\t')[2])) # trust

        # creates string format of word data
        text = ''
        word_emotions = []
        if lexicon[word][0] == 1:
            text += 'positive'
        elif lexicon[word][1] == 1:
            text += 'negative'
        for k in range(2, 10):
            if lexicon[word][k] == 1:
                word_emotions.append(emotions[k])
        if len(word_emotions) != 0:
            text += ' (' + str(word_emotions)[1:-1] + ')'
        if text == '':
            text = 'no emotions attached'
        lexicon[word].append(text)

############################## HELPER METHODS ##############################

# determines the sentiment and its strength in a sentence using nltk Vader
def sentimentValue(words):
    analyze = SentimentIntensityAnalyzer()
    word_str = ' '.join(words)
    score_dict = analyze.polarity_scores(word_str)
    return score_dict

# determines part of speech of a word
def partsOfSpeech(sentence):
    tagged = pos_tag(sentence)
    return tagged

############################## CHARACTERISTIC DICTIONARY ##############################

# creates a dictionary of words across all files, keeping track of:
#    - frequency (occurrences/number of files)
#    - type of sentiment (average sentiment scaled to between -1 and 1)
#    - strength of sentiment (average abs(sentiment) scaled to between 0 and 1)
#    - breadth (number of files found in/number of files total)
#    - phrase length (length of phrase)
#    - raw associated emotions (anger, anticipation, disgust, fear, joy, sadness, surprise, trust)
#    - scaled associated emotions (anger, anticipation, disgust, fear, joy, sadness, surprise, trust)
def characteristicDictionary(pathnames):
    dic = {}
    files_read = 0
    for pathname in pathnames:
        raw = openFile(pathname)
        if raw != '':
            files_read += 1
            sentences = sent_tokenize(raw)

            # phrase extraction (lengths 2-4) initialization
            file_phrases = []
            words = raw.split(' ')
            for word in words:
                stopWords = set(stopwords.words('english'))
                words = [w for w in words if w not in stopWords]
            raw = ' '.join(words)
            #Pull 4 word phrases
            finder = QuadgramCollocationFinder.from_words(words)
            finder.apply_freq_filter(3)
            best = finder.nbest(quadgram_measures.pmi, 5)
            for pair in best:
                pair = ' '.join(pair)
                file_phrases.append(pair.lower())
                raw = raw.replace(pair , '')
            words = raw.split(' ')
            finder = TrigramCollocationFinder.from_words(words)
            finder.apply_freq_filter(3)
            best = finder.nbest(trigram_measures.pmi, 10)
            for pair in best:
                pair = ' '.join(pair)
                file_phrases.append(pair.lower())
                raw = raw.replace(pair, '')
            words = raw.split(' ')
            finder = BigramCollocationFinder.from_words(words)
            finder.apply_freq_filter(3)
            best = finder.nbest(bigram_measures.pmi, 25)
            for pair in best: file_phrases.append(' '.join(pair).lower())



            for phrase in file_phrases:
                if phrase in dic:
                    dic[phrase][3] += 1
                else:
                    phrase_length = len(phrase.split(' '))
                    dic[phrase] = [0, 0, 0, 1, phrase_length, [0, 0, 0, 0, 0, 0, 0, 0]]

            # word/phrase extraction
            file_dic = {}
            for sentence in sentences:
                words = word_tokenize(sentence)
                # corrects for bad formatting
                corrected_words = []
                for i in range(len(words)):
                    word = words[i].lower()
                    if len(word) > 1:
                        if word[-1] not in alph:
                            word = word[:-1]
                    corrected_words.append(word)
                score_dict = sentimentValue(corrected_words)
                val = score_dict['compound']
                sentence_emotions = [0, 0, 0, 0, 0, 0, 0, 0]
                for word in corrected_words:
                    if word in lexicon:
                        for k in range(2, 10):
                            sentence_emotions[k-2] += lexicon[word][k]
                tagged = partsOfSpeech(corrected_words)
                for i in range(len(corrected_words)):
                    pos = ''
                    if tagged[i][1][0] == 'J':
                        pos = 'a'
                    if tagged[i][1][0] == 'N':
                        pos = 'n'
                    if tagged[i][1][0] == 'V':
                        pos = 'v'
                    try:
                        lemma = lemmatizer.lemmatize(tagged[i][0], pos=pos)
                        if tagged[i][1] not in bad_pos_list:
                            if len(lemma) > 2:
                                if lemma not in file_dic.keys():
                                    file_dic[lemma] = 'unseen'
                                if lemma in dic:
                                    dic[lemma][0] += 1
                                    dic[lemma][1] += val
                                    dic[lemma][2] += abs(val)
                                    if file_dic[lemma] == 'unseen':
                                        dic[lemma][3] += 1
                                    dic[lemma][5] = [x+y for x, y in zip(dic[lemma][5], sentence_emotions)]
                                else:
                                    dic[lemma] = []
                                    dic[lemma].append(1)
                                    dic[lemma].append(val)
                                    dic[lemma].append(abs(val))
                                    dic[lemma].append(1)
                                    dic[lemma].append(1)
                                    dic[lemma].append(sentence_emotions)
                                file_dic[lemma] = 'seen'
                    except KeyError:
                        continue
                for phrase in file_phrases:
                    phrase_length = len(phrase.split(' '))
                    count = sentence.lower().count(phrase)*phrase_length
                    dic[phrase][0] += count
                    dic[phrase][1] += count*val
                    dic[phrase][2] += count*abs(val)
                    dic[phrase][5] = [x+y*count for x, y in zip(dic[phrase][5], sentence_emotions)]

    # converts to averages and scales
    max_val = 0
    max_abs_val = 0
    max_emotions = [0, 0, 0, 0, 0, 0, 0, 0]
    for key in dic:
        if dic[key][0] != 0:
            dic[key][1] = dic[key][1]/dic[key][0]
            dic[key][2] = dic[key][2]/dic[key][0]
            # sets max vals to be the largest average sentiment attached to an entry
            if dic[key][1] > max_val:
                max_val = dic[key][1]
            if dic[key][2] > max_abs_val:
                max_abs_val = dic[key][2]
            for n in range(0, 8):
                if dic[key][5][n] > max_emotions[n]:
                    max_emotions[n] = dic[key][5][n]
            # converts to appearances per file and fraction of files appearing in
            dic[key][0] = dic[key][0]/files_read
            dic[key][0] = round(dic[key][0], 2)
            # scales to between 0 and 1
            dic[key][3] = dic[key][3]/files_read
            dic[key][3] = round(dic[key][3], 2)
    for key in dic:
        if dic[key][0] != 0:
            # scales to between -1 and 1
            dic[key][1] = dic[key][1]/max_val
            dic[key][1] = float(round(dic[key][1], 2))
            if dic[key][1] <= .01:
                dic[key][1] = 0
            # scales to between 0 and 1
            dic[key][2] = dic[key][2]/max_abs_val
            dic[key][2] = float(round(dic[key][2], 2))
            if dic[key][2] <= .01:
                dic[key][2] = 0
            # scales to between 0 and 1
            dic[key].append([0, 0, 0, 0, 0, 0, 0, 0])
            for n in range(0, 8):
                dic[key][6][n] = dic[key][5][n]/max_emotions[n]
                dic[key][6][n] = float(round(dic[key][6][n], 2))
                if dic[key][6][n] <= .01:
                    dic[key][6][n] = 0
    return dic

############################## DETERMINING KEYWORDS AND TROPES ##############################

# returns keywords, based on the frequency of each word per file and number of
# files appeared in, expressed as a percentage
def searchKeywords(dic, minimum_freq, minimum_breadth):
    keywords = []
    for key in dic:
        if dic[key][0] >= minimum_freq and dic[key][3] >= minimum_breadth:
            keywords.append((key, dic[key][0], dic[key][3], dic[key][5], dic[key][6]))
    keywords = sorted(keywords, key=itemgetter(2), reverse=True)
    return keywords

# returns potential tropes and their average sentiment from the list of keywords
# that meet minimum sentiment strength or minimum emotion set by user
def searchTropes(dic, keywords, minimum_sentiment_strength, min_emotion):
    tropes = []
    keywords = [info[0] for info in keywords]
    for word in keywords:
        if dic[word][2] > minimum_sentiment_strength or max(dic[word][5]) > min_emotion:
            tropes.append((word, dic[word][1], dic[word][2], dic[word][5], dic[word][6]))
    tropes = sorted(tropes, key= itemgetter(2), reverse=True)
    return tropes

############################## CREATING POLYGONS ##############################

# creates a radar chart for a trope given its associated emotions
def createPolygon(trope, scaled_emotions, source_dir):
    out_dir = source_dir + 'out/'
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    file_name = out_dir + ''.join(random.choices(string.ascii_letters, k= 20)) + '.png'
    file_name = file_name.replace(' ', '_')
    graph(trope, emotions[2:], scaled_emotions, optimum, file_name)
    return file_name

############################## MAIN METHOD ##############################
'''
if __name__ == '__main__':
    # finds keywords and tropes
    readLexicon() # put into static folder
    pathnames = getFilesRecurse('corpus') # This should be a variable in the UI: user uploads multiple files, I put them in a 'temporary' folder, then point to that folder. Eventually we'll get folder uploads hopefully
    dic = characteristicDictionary(pathnames)
    keywords = searchKeywords(dic, .5, .05) # not sure if these constants should be customizable
    tropes = searchTropes(dic, keywords, .5, 40) # likewise
    for trope in tropes:
        print(trope)

    # creates polygon graphs
    for item in tropes:
        createPolygon(item[0], item[4]) # saves image'''

def generate(source_dir, chosen_tropes):

    # creates polygon graphs
    if chosen_tropes == None:
        return
    image_list = []
    for item in chosen_tropes:
        image_list.append(createPolygon(item[0], item[4], source_dir)) # saves image
    for image in image_list:
        os.chmod(image, 0o644)
    return image_list

def tropes(source_dir): # display all possible tropes the user can pick
    if source_dir == None:
        return
    readLexicon()
    pathnames = getFilesRecurse(source_dir)
    dic = characteristicDictionary(pathnames)
    keywords = searchKeywords(dic, .5, .05) # not sure if these constants should be customizable
    tropes = searchTropes(dic, keywords, .45, 30) # likewise
    return tropes
