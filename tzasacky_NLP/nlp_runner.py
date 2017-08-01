################ NLP Runner ##################
# This will be the program that runs all NLP #
# routines. It will call different NLP tools #
# depending on language and function             #
##############################################

from collections import defaultdict
import nltk
import networkx
from newspaper import Article
import json
import math
from nltk import sentiment
import pandas as pd
import matplotlib.pyplot as plt
from tzasacky_NLP import language_detector, file_io, radar, spacy_nlp, sentiment
import jgraph
import time
import os.path
import tempfile
import csv



############ Low Level Functions #############

def getTexts(directory):
    # Input: Directory
    # Output:List of all text files in the directory fully loaded into memory
    texts = []
    pathnames = file_io.getFilesRecurse(directory, '.txt')
    for pathname in pathnames:
        texts.append(file_io.openFile(pathname))
    return texts

def getArticles(urls):
    #Input: URLS of news articles
    #Output: Article objects --> use article.text for parsing etc. with SpaCy, others are useful metadata
    articles = []
    for url in urls:
        article = Article(url)
        article.download()
        article.parse()
        articles.append(article)
    return articles

def languageDict(texts):
    # Input: text documents
    # Output: dictionary of documents keyed by language
    dic = defaultdict(list)
    for text in texts:
        language = language_detector.stopword_detect_language(text)
        dic[language].append(text)
    return dic


def loadAllModels(languages):
    # Input: list of languages
    # Output: dictionary of models keyed by language
    languageModels = defaultdict()
    for language in languages:
        # Spacy Parsing
        if language == 'english':
            nlp = spacy_nlp.loadModel('en')
            languageModels[language] = nlp
            # other languages will need similar branching
            # spacy will likely differ from syntaxnet slightly
    return languageModels


def parseTexts(texts, models):
    # Inputs: dictionaries of language models and texts (same keys)
    # Returns a dict of parsed documents keyed by language
    languages = texts.keys()
    dict = defaultdict(list)
    for language in languages:
        if language == 'english':
            docs = spacy_nlp.pipeline(models[language], texts[language])
            dict[language] = docs
    return dict

def readLexicon():
    #No input because it only works for this one lexicon
    #f = open('static/lexicon.txt', 'r')
    import os
    print(os.getcwd())
    f = open('tzasacky_NLP/lexicon.txt')
    raw = f.read().split('\n')
    lexicon = {}
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
    return lexicon

################# JSON Serialization ##################

def marshall(object):
    return json.dumps(object)

def unmarshall(object):
    return json.loads(object)

def csvInfo(entityUsages):
    labels = {}
    for key in entityUsages.keys():
        for label in entityUsages[key]:
            if label in labels:
                if len(entityUsages[key][label]) > labels[label]:
                    labels[label] = len(entityUsages[key][label])
            else: labels[label] = len(entityUsages[key][label])
    return labels

def csvWrite(entityUsages):
    info = csvInfo(entityUsages)
    header = ['Actor']
    headerRef = []
    for label, columns in info.items():
        headerRef.append((label, columns))
        i = 0
        while i < columns:
            header.append(label)
            i += 1
    with open('sheet.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow(header)
        for key in entityUsages.keys():
            row = [key]
            for label, columns in headerRef:
                added = 0
                if label in entityUsages[key].keys():
                    for entity in entityUsages[key][label].keys():
                        added += 1
                        row.append(entity)
                while added < columns:
                    row.append('')
                    added += 1
            writer.writerow(row)




################# Feature Functions ################

def preProcess(texts):
    # Input: Texts
    # Output: A language-keyed dictionary of fully tokenized, tagged, and parsed documents.
    textDict = languageDict(texts)
    languages = dict.keys(textDict)
    modelDict = loadAllModels(languages)
    parsedDocs = parseTexts(textDict, modelDict)
    return parsedDocs


def crossEntitySentiment(docs, central_type = None):
    #Input: Spacy parsed docs
    #Output: Nested dictionary with sentiments between entities
    entitySentences = spacy_nlp.crossEntityUsages(docs, central_type)
    for key in entitySentences.keys():
        for label in entitySentences[key].keys():
            for keytwo in entitySentences[key][label].keys():
                sentences = [sent.text for sent in entitySentences[key][label][keytwo]]
                sentiments = sentiment.VaderSentiment(sentences)
                neg, neu, pos, comp = 0, 0, 0, 0
                for sent in sentiments:
                    neg += sent['neg']
                    neu += sent['neu']
                    pos += sent['pos']
                    comp += sent['compound']
                uses = len(sentiments)
                neg = neg / uses
                neu = neu / uses
                pos = pos / uses
                comp = comp / uses
                entitySentences[key][label][keytwo] = (neg, neu, pos, comp, len(sentiments))
    return entitySentences

def emotionalMultiValences(docs, lexicon):
    entitySentences = spacy_nlp.crossEntityUsages(docs)
    for key in entitySentences.keys():
        for label in entitySentences[key].keys():
            for keytwo in entitySentences[key][label].keys():
                sentences = [sent for sent in entitySentences[key][label][keytwo]]
                emotion = sentiment.emotionScore(sentences, lexicon)
                entitySentences[key][label][keytwo] = emotion
    #NOTE: This is an absolute scale. It's based on emotion/word. Display as percentages?
    #      Scaling it around 1 is a problem. Ask Tony Wednesday.
    return entitySentences

################## Display Functions ####################

def docSummary(docs):
    #Input: parsed docs
    #Output: Basic statistics. Number of docs, (path of) histogram of doc length distribution, total word count
    num = len(docs)
    lengths = []
    totLength = 0
    for doc in docs:
        length = len(doc)
        lengths.append(length)
        totLength += length
    lengths = sorted(lengths)
    max = lengths[0]
    min = lengths[(len(lengths)-1)]
    #Histogram Creation
    plt.figure(figsize=(12, 9))
    # Remove plot frame lines
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # Axis ticks only bottom and left
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Document Length (Words)", fontsize=16)
    plt.ylabel("Count (Documents)", fontsize=16)
    # Plot histogram. Bin number might need tweaking.
    plt.hist(lengths, edgecolor= 'black', color= '#3ad43f', bins= 10)
    # Save as PNG. bbox_inches="tight" removes all extra whitespace on edges of plot
    f = tempfile.NamedTemporaryFile(dir='static/temp', suffix='.png', delete=False)
    # save the figure to the temporary file
    plt.savefig(f, bbox_inches='tight')
    f.close()  # close the file
    # get the file's name
    # (the template will need that)
    path = f.name.split('/')[-1]
    path = path.split('\\')[-1]

    return num, path, totLength

def entitySentiment(docs):
    #Input: Directory of .txt files to analyse
    #Output: Dictionary of relevant entities and their associated sentiment
    #Methodology: Sentiment towards an entity is approximated as sentiment averaged
    #                     over all of the sentences they appear in
    entityInfo = []
    entitySentences = spacy_nlp.improvesUsages(docs)
    for label in entitySentences.keys():
        for entity in entitySentences[label]:
            #Take text of sentences, entries in dict are spacy span objects
            sentences = [e.text for e in entitySentences[label][entity]]
            sentiments = sentiment.VaderSentiment(sentences)
            #Build combined sentiment by averaging individual sentence sentiments
            neg, neu, pos, comp = 0,0,0,0
            for sent in sentiments:
                neg += sent['neg']
                neu += sent['neu']
                pos += sent['pos']
                comp += sent['compound']
            uses = len(sentiments)
            neg = neg/uses
            neu = neu/uses
            pos = pos/uses
            comp = comp/uses
            #List of lists will be used for sortable html table
            #Filter out ones with low sentiment or low usage so that there's a reasonable number
            if uses > 1:
                entityInfo.append([entity, "%.2f" % neg, "%.2f" % neu, "%.2f" % pos, "%.2f" % comp, uses])
    return entityInfo


def sentimentGraph(docs):
    #Input: spacy parsed docs
    #Output: graph with cross-entity sentiment on edges
    crossEnt  = crossEntitySentiment(docs)
    graph = networkx.Graph()
    for k1 in crossEnt.keys():
        for k2 in crossEnt[k1].keys():
            graph.add_edge(k1, k2, sentiment = crossEnt[k1][k2][3])
    return graph


def emotionalValences(docs, lexicon):
    # Formerly what built the tropes
    # Input: docs, the emotional lexicon
    # Output: Radar charts to be displayed (paths to their pictures)
    paths = []
    emotionScores = []
    emotionLabels = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
    entitySentences = spacy_nlp.improvesUsages(docs)
    max = 0
    for label in entitySentences.keys():
        for ent in entitySentences[label].keys():
            sentences = entitySentences[label][ent]
            if(len(sentences) > 1):
                scores = sentiment.emotionScore(sentences, lexicon)
                # We'll need to scale off max emotion later
                for score in scores:
                    if score > max: max = score
                emotionScores.append((ent, scores))
    optimum = [max, max, max, max, max, max, max, max]
    # Now we have, entities, scores, labels, and optimums. We can create the radar graphs
    for ent, scores in emotionScores:
        # Save the file in the temp folder
        f = tempfile.NamedTemporaryFile(dir='static/temp', suffix='.png', delete=False)
        radar.graph(trope=ent, values=scores, labels=emotionLabels, optimum=optimum, file_name=f)

        # get the file's name (the template will need that)
        path = f.name.split('/')[-1]
        path = path.split('\\')[-1]
        paths.append(path)
    return paths

def sourceAnalysis(articles):
    return


if __name__ == '__main__':
    st = time.time()
    texts = getTexts('corpus')
    parsedDocs = preProcess(texts)
    docs = parsedDocs['english']
    sent = crossEntitySentiment(docs, 'PERSON')
    csvWrite(sent)
    #lexicon = sentiment.readLexicon()
    #e = emotionalValences(docs, lexicon)
    print(time.time() - st)
    #graph = sentimentGraph(docs)
    #graph = jgraph.draw(graph)
    #f = open("yourpage.html", "w")
    #f.write(graph)
    #f.close()


    #graph = sentimentGraph(docs)
    #sna = SNA.SNA
    #sna.G = graph
    

    #graph = spacy_nlp.entityGraph(docs)
    #print(graph.edges())
    #SENTIMENT TESTING
    #entities = spacy_nlp.namedEntities(docs, True)
    #spacy_nlp.crossEntitySentiment(entities)
    #for doc in docs:
    #   sentences = [s.text for s in doc.sents]
    #   print(sentiment.VaderSentiment(sentences))
    #GRAPH TESTING
    #graph = spacyNLP.entityGraph(docs)
    #json = marshall(graph)
#TODO: Understand what will go into NLP box, build it all, format it right, etc.
#Overall Summary: Number of Docs. Document length distribution (histogram of document lengths). Total word count.
    #FUNCTION: docSummary returns num. docs, doc lengths (potentially direct to histogram later), total word count.

#Entity analysis: Only give 100 per page or something like that
    # Open new box with top N refined entities analyzed. Sortable Fields -> Entity Name, Sentiment, Number of appearances
    #FUNCTION: EntitySentiment give us entity names, number of uses, sentiment
    #          Need to turn it into an HTML Table. Include Pictures.
    # Visual analysis: Lexical dispersion plot. Radar charts.
    #FUNCTION: Current radar chart implementation. LDP implementation existing can be run on the text.
#Source Analysis: No separate box.
    #If didn't use url scraper - Message explaining
    #Else - Pie chart of docs by source.
        #List of sources: Subjectivity score. Date range of articles. Most informative articles?
        #Most mentioned entities and sentiment towards (Common subjects).

#Network Analysis: Cross entity sentiment
    # MAKE SURE GRAPH IS UNDIRECTED
    # List of entity types --> Which should be included as nodes? Color nodes based on type.
    # Open new box running JGraph. With sentiment between. Legend if possible of node types.

#Geospatial Analysis: Open separate box
    #Depends on mordecai implementation. Location tagging. Test implementation could just be dots that get larger
    # as a location is recognized more

#Word clouds?
