from gat.service import NLP_OTHER

def getNLPOTHER(file):
	nlp_stemmerize = NLP_OTHER.stemmerize(file)
	nlp_lemmatize = NLP_OTHER.lemmatize(file)
	nlp_abstract = NLP_OTHER.abstract(file)
	nlp_top20_verbs = NLP_OTHER.top20_verbs(file)
	nlp_top20_persons = NLP_OTHER.top20_persons(file)
	nlp_top20_locations = NLP_OTHER.top20_locations(file)
	nlp_top20_organizations = NLP_OTHER.top20_organizations(file)
	nlp_sentence_sentiment_distribution = NLP_OTHER.sentence_sentiment_distribution(file)
	nlp_wordcloud = NLP_OTHER.wordcloud(file)
	return nlp_stemmerize, nlp_lemmatize, nlp_abstract, nlp_top20_verbs, nlp_top20_persons, nlp_top20_locations, nlp_top20_organizations, nlp_sentence_sentiment_distribution, nlp_wordcloud