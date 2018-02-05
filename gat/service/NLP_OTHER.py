from gat.service.SVO_SENT_MODULE_spacy import SVOSENT
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import data
import pandas as pd
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import matplotlib.colors as colorlib
import matplotlib.cm as cmx
import numpy as np
import nltk
import spacy
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import matplotlib as mpl
from gensim.summarization import summarize
from gat.dao import dao

##NLP functions

def wordcloud(txt_name):
    with open(txt_name, 'r') as myfile:
        article=myfile.read().replace('\n', '')
    mpl.rcParams['font.size']=12                #10 
    mpl.rcParams['savefig.dpi']=100             #72 
    mpl.rcParams['figure.subplot.bottom']=.1 
    
    
    stopwords = set(STOPWORDS)
    
    wordcloud = WordCloud(
                              background_color='white',
                              stopwords=stopwords,
                              max_words=200,
                              max_font_size=40, 
                              random_state=42
                             ).generate(article)
    
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis('off')
    filename = 'out/nlp/nlp_wordcloud.png'
    plt.savefig(filename, dpi=100)
    return filename


def stemmerize(txt_name):
    sno = nltk.stem.SnowballStemmer('english')
    with open(txt_name, 'r') as myfile:
        article=myfile.read().replace('\n', '')
    words=article.split(' ')
    results=[]
    for word in words:
        results.append(sno.stem(word))
    return ' '.join(results)

def lemmatize(txt_name):
    nlp = dao.spacy_load_en()
    with open(txt_name, 'r') as myfile:
        article=myfile.read().replace('\n', '')
    results=[]
    for token in nlp(article):
        results.append(token.lemma_)
    return ' '.join(results)

def abstract(txt_name):
    with open(txt_name, 'r') as myfile:
        article=myfile.read().replace('\n', '')
    return summarize(article,ratio=0.2)

def top20_verbs(txt_name):
    nlp = dao.spacy_load_en()
    with open(txt_name, 'r') as myfile:
        article=myfile.read().replace('\n', '')
    results=[]
    for token in nlp(article):
        if token.pos_=='VERB':
            results.append(token.lemma_)
    results=[e for e in results if e not in ['will','would','could','may','can']]
    counts = Counter(results)
    labels, values = zip(*counts.items())
    indSort = np.argsort(values)[::-1]
    if len(indSort)>20:
        indSort=indSort[:19]
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]
    
    indexes = np.arange(len(labels))
    
    bar_width = 0.35
    plt.figure() 
    plt.bar(indexes, values)
    
    # add labels
    plt.xticks(indexes + bar_width, labels,rotation=45)
    plt.show()
    plt.savefig("out/nlp/nlp_top20_verbs.png", dpi=100)
    return "out/nlp/nlp_top20_verbs.png"
    
def top20_persons(txt_name):
    nlp = dao.spacy_load_en()
    with open(txt_name, 'r') as myfile:
        article=myfile.read().replace('\n', '')
    parsed_phrase=nlp(article)
    results=[]
    names = list(parsed_phrase.ents)
    for e in names:
        if e.label_== 'PERSON':
                results.append(e.text)
    counts = Counter(results)
    labels, values = zip(*counts.items())
    indSort = np.argsort(values)[::-1]
    if len(indSort)>20:
        indSort=indSort[:19]
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]
    
    indexes = np.arange(len(labels))
    
    bar_width = 0.35
    plt.figure() 
    plt.bar(indexes, values)
    
    # add labels
    plt.xticks(indexes + bar_width, labels,rotation=90)
    plt.show()
    plt.savefig("out/nlp/top20_persons.png", dpi=100)
    return "out/nlp/top20_persons.png"
    
def top20_locations(txt_name):
    nlp = dao.spacy_load_en()
    with open(txt_name, 'r') as myfile:
        article=myfile.read().replace('\n', '')
    parsed_phrase=nlp(article)
    results=[]
    names = list(parsed_phrase.ents)
    for e in names:
        if e.label_== 'GPE'or e.label=='LOC':
                results.append(e.text)
    counts = Counter(results)
    labels, values = zip(*counts.items())
    indSort = np.argsort(values)[::-1]
    if len(indSort)>20:
        indSort=indSort[:19]
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]
    
    indexes = np.arange(len(labels))
    
    bar_width = 0.35
    plt.figure() 
    plt.bar(indexes, values)
    
    # add labels
    plt.xticks(indexes + bar_width, labels,rotation=90)
    plt.show()
    plt.savefig("out/nlp/top20_locations.png", dpi=100)
    return "out/nlp/top20_locations.png"
    
def top20_organizations(txt_name):
    nlp = dao.spacy_load_en()
    with open(txt_name, 'r') as myfile:
        article=myfile.read().replace('\n', '')
    parsed_phrase=nlp(article)
    results=[]
    names = list(parsed_phrase.ents)
    for e in names:
        if e.label_== 'ORG':
                results.append(e.text)
    counts = Counter(results)
    labels, values = zip(*counts.items())
    indSort = np.argsort(values)[::-1]
    if len(indSort)>20:
        indSort=indSort[:19]
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]
    
    indexes = np.arange(len(labels))
    
    bar_width = 0.35
    plt.figure() 
    plt.bar(indexes, values)
    
    # add labels
    plt.xticks(indexes + bar_width, labels,rotation=90)
    plt.show()
    plt.savefig("out/nlp/top20_organizations.png", dpi=100)    
    return "out/nlp/top20_organizations.png"


def sentence_sentiment_distribution(txt_name):
    sent_detector = data.load('tokenizers/punkt/english.pickle')
    sid=SentimentIntensityAnalyzer()
    with open(txt_name, 'r') as myfile:
        article=myfile.read().replace('\n', '')
    sentences = sent_detector.tokenize(article)
    sentiments=[]    
    for sen in sentences:
        emotion=sid.polarity_scores(text=sen)['compound']
        if emotion<=1.0 and emotion>0.75:
            sentiments.append('very positive')
        if emotion<=0.75 and emotion>0.25:
            sentiments.append('positive')
        if emotion<=0.25 and emotion>-0.25:
            sentiments.append('neutral')
        if emotion<=-0.25 and emotion>-0.75:
            sentiments.append('negative')
        if emotion<=-0.75 and emotion>=-1.0:
            sentiments.append('very negative')
    counts = Counter(sentiments)
    labels=['very negative','negative', 'neutral','positive','very positive']
    values=[counts['very negative'],counts['negative'],counts['neutral'],counts['positive'],counts['very positive']]
    indexes = np.arange(len(labels))
    
    bar_width = 0.35
    plt.figure() 
    plt.bar(indexes, values)

    # add labels
    plt.xticks(indexes + bar_width, labels, rotation=45)
    plt.show()
    plt.savefig("out/nlp/sentence_sentiment_distribution.png", dpi=100)    
    return "out/nlp/sentence_sentiment_distribution.png"
    


