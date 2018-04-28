from gat.core.nlp import language_detector, nlp_runner, parser, radar, scraper, sentiment, spacy_nlp
from gat.nltk.Memory_Tests import NLP_OTHER


def create_expected(file_name):
    f = open(str('gat/nltk/Memory_Tests/removed_corpora/' + file_name + ".txt"), 'w+')
    num_articles = 10
    test_articles = [('gat/nltk/Memory_Tests/Articles/article' + str(x) + '.txt') for x in range(1, num_articles + 1)]
    for article in test_articles:
        f.write("{} stemmerize: \n".format(article[31:]))
        f.write(NLP_OTHER.stemmerize(article))
        f.write("\n\n")

        f.write("{} lemmatize: \n".format(article[31:]))
        f.write(NLP_OTHER.lemmatize(article))
        f.write("\n\n")

        f.write("{} sentence_sentiment_distribution: \n".format(article[31:]))
        f.write("".join(NLP_OTHER.sentence_sentiment_distribution(article)))
        f.write("\n\n")

        f.write("{} quote_extractor: \n".format(article[31:]))
        f.write("".join(NLP_OTHER.quote_extractor(article)))
        f.write("\n\n")

        f.write("{} stop_word_filter: \n".format(article[31:]))
        f.write("".join(NLP_OTHER.stop_word_filter(article)))
        f.write("\n\n")

        f.write("{} calculate_stopword_frequency: \n".format(article[31:]))
        f.write("".join(language_detector.calculate_stopword_frequencies(article)))
        f.write("\n\n")

        f.write("=" * 60 + "\n\n")

    f.close()


#create_expected('expected')