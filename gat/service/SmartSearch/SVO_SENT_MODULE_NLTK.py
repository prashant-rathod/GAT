#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 19:53:39 2017

@author: ruobingwang
"""
import os
import pandas as pd
from nltk.parse.stanford import StanfordParser
from nltk.tree import ParentedTree, Tree
from nltk import data
from gat.service.SmartSearch import file_io
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datefinder

# change the dir for stanford NLP parser,
# download Stanford NLP parser at https://nlp.stanford.edu/software/lex-parser.shtml#Download
os.environ[
    'STANFORD_PARSER'] = '/media/ruobingwang/5860227760225C4E/LUCAS/Ruobing_NLP/stanford-parser-full-2017-06-09/stanford-parser.jar'
os.environ[
    'STANFORD_MODELS'] = '/media/ruobingwang/5860227760225C4E/LUCAS/Ruobing_NLP/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'


class SVOSENT(object):
    """
    Class Methods to Extract Subject Verb Object Tuples from a Sentence
    """

    def __init__(self, language='english'):
        """
        Initialize 
        """
        self.parser = StanfordParser()
        self.sent_detector = data.load('tokenizers/punkt/' + language + '.pickle')
        self.analyzer = SentimentIntensityAnalyzer()

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
        result = [text[text.find("Full text:") + 10:text.find("Publication title")] for text in textlist if
                  len(text) != 0]
        return result

    # find all ancestors of a subtree
    def find_ancestors(self, t):
        parents = []

        def find(t):
            parents.append(t.parent().label())
            if t.parent().label() == 'ROOT':
                return parents
            else:
                return find(t.parent())

        result = find(t)
        return result

        # Search for NN, NNP, PRP etc in subtrees based on some restrictions

    def find_subject(self, t):
        subjects = []
        for a in t.subtrees(lambda t: t.label() == 'S' and t.parent().label() not in ['S']):
            for s in a.subtrees(lambda a: a.label() == 'NP' and a.parent().label() != 'VP'):
                for n in s.subtrees(lambda n: n.label() in ['NN', 'NNP', 'NNS', 'PRP'] and len(
                        set(self.find_ancestors(n)).intersection(['VP'])) == 0):
                    subjects.append(n[0])
        return list(set(subjects))

    # Depth First Search the tree and take verbs in VP subtree.
    def find_predicate(self, t):
        v = None
        predicates = []
        for s in t.subtrees(lambda t: t.label() == 'VP'):
            for n in s.subtrees(lambda n: n.label().startswith('VB')):
                v = n
                predicates.append(v[0])
        return list(set(predicates))

    def find_object(self, t):
        objects = []
        for s in t.subtrees(lambda t: t.label() == 'VP'):
            for n in s.subtrees(lambda n: n.label() in ['NP', 'PP', 'ADJP']):
                if n.label() in ['NP', 'PP']:
                    for c in n.subtrees(lambda c: c.label().startswith('NN')):
                        objects.append(c[0])
        return list(set(objects))

    def sentence_split(self, text):
        """
        split article to sentences
        """
        sentences = self.sent_detector.tokenize(text)
        return sentences

    def get_svo(self, sent):
        t = list(self.parser.raw_parse(sent))[0]
        t = ParentedTree.convert(t)
        return {'Subjects': self.find_subject(t),
                'Predicates': self.find_predicate(t),
                'Objects': self.find_object(t),
                'Sentence': sent}

    # return a dataframe
    def get_svo_from_article(self, article):
        sentences = self.sentence_split(article)
        val = []
        for sent in sentences:
            svoresult = self.get_svo(sent)
            val.append(svoresult)
        return pd.DataFrame(val)

    ####################################################
    # below are the functions for sentiment analysis

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
        try:
            date = list(datefinder.find_dates(article))[0]
        except:
            date = '------'
        sentences = self.sentence_split(article)
        val1 = []
        val2 = []

        for sent in sentences:
            val1.append(self.sentimentAnalysis(sent))
            val2.append(self.get_svo(sent))
        result = pd.merge(pd.DataFrame(val1), pd.DataFrame(val2), on='Sentence')[
            ['Sentence', 'Subjects', 'Predicates', 'Objects', 'compound', 'pos', 'neu', 'neg']]
        try:
            result['date'] = date
        except:
            result['date'] = '-----'
        if subject == None:
            return result
        else:
            return result[result['Subjects'].apply(lambda x: subject in x)]


if __name__ == "__main__":
    svo_sent = SVOSENT('chinese')
    article = "美国攻击伊拉克."
    result = svo_sent.svo_senti_from_article(article)
    print(result)

    '''
    articles_not=svo_sent.getTexts('corpus2')[0]
    articles=svo_sent.split_and_clean(articles_not)
    import time
    t0=time.time()
    results=[]
    for i,article in enumerate(articles):
        result=svo_sent.svo_senti_from_article(article)
        results.append(result)
        print(i,end='th/')
        print(len(articles),end='')
        print(' article is done')
    #result2=svo_sent.svo_senti_from_article(article,'Robin')
    t1=time.time()
    results=pd.concat(results, axis=0)
    print(t1-t0)
    print(results)
    svo_sent.WriteCSV(results,'Iran_dataset')
    '''

    # to do: improve speed by using better algorithm in trees.
