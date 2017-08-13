nlp_summary, nlp_entities, nlp_network, nlp_sources, nlp_tropes = None, None, None, None, None
if NLP_dir:
    texts = nlp_runner.getTexts(NLP_dir)
    parsedDocs = nlp_runner.preProcess(texts)
    docs = parsedDocs['english']
    lexicon = nlp_runner.readLexicon()
    nlp_summary = nlp_runner.docSummary(docs)
    nlp_entities = nlp_runner.entitySentiment(docs)
    nlp_network = nlp_runner.sentimentGraph(docs)
    nlp_tropes = nlp_runner.emotionalValences(docs, lexicon)

if NLP_urls:
    articles = nlp_runner.getArticles(NLP_urls)
    texts = [article.text for article in articles]
    parsedDocs = nlp_runner.preProcess(texts)
    docs = parsedDocs['english']
    lexicon = nlp_runner.readLexicon()
    nlp_summary = nlp_runner.docSummary(docs)
    nlp_entities = nlp_runner.entitySentiment(docs)
    # nlp_network = nlp_runner.sentimentGraph(docs)
    nlp_sources = nlp_runner.sourceAnalysis(articles)
    nlp_tropes = nlp_runner.emotionalValences(docs, lexicon)

#################James WU's NLP methods:###########################
nlp_sentiment = None
if NLP_file_sentiment != None:
    import os.path

    if not os.path.isfile("nb_sentiment_classifier.pkl"):
        nlp_james.trainSentimentClassifier()
    with open(NLP_file_sentiment) as file:
        nlp_sentiment = nlp_james.predictSentiment(file.read())
####### To perform sentiment analysis on scraped data from URL - Ryan Steed 7 Jun 2017 #####
'''
if research_question[3] != None:
    print("Analyzing research question")
    import os.path
    if not os.path.isfile("nb_sentiment_classifier.pkl"):
        nlp_james.trainSentimentClassifier()
    nlp_sentiment = nlp_james.predictSentiment(research_question[3])
'''
######Temporarily turned off as per Tony's request:##################
ner = None
if NLP_NER_sentence != None and NLP_NER_sentence.strip() != "":
    tags = nlp_james.npChunking(NLP_NER_sentence)
    ner = nlp_james.treeTraverseString(tags)
# if request.method == 'POST':

iob = None
if NLP_IOB_sentence != None:
    ne_tree = nlp_james.NEChunker(NLP_IOB_sentence)
    iob = nlp_james.IOB_Tagging(ne_tree)
######Temporarily turned off as per Tony's request##################
#################James WU's NLP methods###########################

###########scrape inputted url and return text:##############
if research_question != None and research_question.strip() != "":
    print("RESEARCH QUESTION: " + research_question)
    research_question = url_parser.write_articles([research_question.strip()])

research_question = research_question if research_question != None else None
nlp_data_show = nlp_sentiment != None or ner != None or iob != None
