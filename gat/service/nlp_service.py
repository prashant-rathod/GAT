import os.path

from gat.core.nlp import nlp_runner, parser


def nlp_dir(NLP_dir):
    return nlp(NLP_dir, True)


def nlp_urls(NLP_urls):
    return nlp(NLP_urls, False)


def nlp(input, dir):
    nlp_summary, nlp_entities, nlp_network, nlp_sources, nlp_tropes = None, None, None, None, None
    if input is not None:
        texts = None
        articles = None
        if not dir:
            articles = nlp_runner.getArticles(input)
            texts = [article.text for article in articles]
        else:
            texts = nlp_runner.getTexts(input)
        parsedDocs = nlp_runner.preProcess(texts)
        docs = parsedDocs['english']
        lexicon = nlp_runner.readLexicon()
        nlp_summary = nlp_runner.docSummary(docs)
        nlp_entities = nlp_runner.entitySentiment(docs)
        nlp_tropes = nlp_runner.emotionalValences(docs, lexicon)
        if dir:
            nlp_network = nlp_runner.sentimentGraph(docs)
        else:
            nlp_sources = nlp_runner.sourceAnalysis(articles)
    return nlp_summary, nlp_entities, nlp_network, nlp_sources, nlp_tropes


def sentiment(NLP_file_sentiment):
    nlp_sentiment = None
    if NLP_file_sentiment != None:
        if not os.path.isfile("static/resources/nlp/nb_sentiment_classifier.pkl"):
            parser.trainSentimentClassifier()
        with open(NLP_file_sentiment) as file:
            nlp_sentiment = parser.predictSentiment(file.read())
    return nlp_sentiment


def ner(NLP_NER_sentence):
    ner = None
    if NLP_NER_sentence != None and NLP_NER_sentence.strip() != "":
        tags = parser.npChunking(NLP_NER_sentence)
        ner = parser.treeTraverseString(tags)
    return ner


def iob(NLP_IOB_sentence):
    iob = None
    if NLP_IOB_sentence != None:
        ne_tree = parser.NEChunker(NLP_IOB_sentence)
        iob = parser.IOB_Tagging(ne_tree)
    return iob
