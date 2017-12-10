from gat.core.nlp import language_detector, nlp_runner, parser, radar, scraper, sentiment, spacy_nlp
from gat.nltk.Memory_Tests import NLP_OTHER

test_articles = ['article1.txt', 'article2.txt', 'article3.txt', 'article4.txt', 'article5.txt', 'article6.txt',
                 'article7.txt', 'article8.txt', 'article9.txt', 'article10.txt']

f = open('expected.txt', 'w')
for article in test_articles:
    f.write("{} stemmerize: \n".format(article))
    f.write(NLP_OTHER.stemmerize(article))
    f.write("\n\n")

    f.write("{} lemmatize: \n".format(article))
    f.write(NLP_OTHER.lemmatize(article))
    f.write("\n\n")

    f.write("{} sentence_sentiment_distribution: \n".format(article))
    f.write("".join(NLP_OTHER.sentence_sentiment_distribution(article)))
    f.write("\n\n")

    f.write("{} quote_extractor: \n".format(article))
    f.write("".join(NLP_OTHER.quote_extractor(article)))
    f.write("\n\n")

    f.write("{} stop_word_filter: \n".format(article))
    f.write("".join(NLP_OTHER.stop_word_filter(article)))
    f.write("\n\n")

    f.write("{} calculate_stopword_frequency: \n".format(article))
    f.write("".join(language_detector.calculate_stopword_frequencies(article)))
    f.write("\n\n")

f.close()
