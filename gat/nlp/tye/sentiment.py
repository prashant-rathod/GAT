################Sentiment Builder####################
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from sklearn.externals import joblib
from nltk.tokenize import regexp

def trainSubjectivity():
	#Subjective vs. objective sentence classifier. Borrows from NLTK Documentation.
	#Plan on using it in larger machine learning sentiment model as pre-processing
	#Must differentiate between objective and subjective
	subjDocs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')]
	objDocs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')]
	nSubj = len(subjDocs)
	nObj = len(objDocs)
	#90% Training, 10% Test
	subjTrain = int(.9*nSubj)
	objTrain = int(.9*nObj)
	trainSubj = subjDocs[:subjTrain]
	testSubj = subjDocs[subjTrain:nSubj]
	trainObj = objDocs[:objTrain]
	testObj = objDocs[objTrain:nObj]
	trainDocs = trainSubj + trainObj
	testDocs = testSubj + testObj
	#Create sentiment class, mark negation, create features (unigram)
	sentiment = SentimentAnalyzer()
	markNegation = sentiment.all_words([mark_negation(doc) for doc in trainDocs])
	unigramFeats = sentiment.unigram_word_feats(markNegation, min_freq=4)
	sentiment.add_feat_extractor(extract_unigram_feats, unigrams=unigramFeats)
	training = sentiment.apply_features(trainDocs)
	testing = sentiment.apply_features(testDocs)
	#Train classifier
	trainer = NaiveBayesClassifier.train
	subjectivityClassifier = sentiment.train(trainer, training)
	joblib.dump(subjectivityClassifier, 'subjectivity.pkl')
	for key, value in sorted(sentiment.evaluate(testing).items()): print('{0}: {1}'.format(key, value))
	''' 
	RESULTS:
	Accuracy: 0.917
	F - measure[obj]: 0.9164149043303123
	F - measure[subj]: 0.9175769612711023
	Precision[obj]: 0.922920892494929
	Precision[subj]: 0.9112426035502958
	Recall[obj]: 0.91
	Recall[subj]: 0.924
	'''

def subjectivityScore(docs):
	#Input: SpaCy doc class
	#Output: Subjectivity score of document (percent of sentences considered subjective)
	#Note: takes a few minutes the first time, to train classifier. After takes a few seconds.
	word_tokenizer = regexp.WhitespaceTokenizer()
	try:
		sentiment = load('sa_subjectivity.pickle')
	except LookupError:
		sentiment = demo_subjectivity(NaiveBayesClassifier.train, True)
	subjectivities = []
	for doc in docs:
		tot, subj = 0,0
		for sent in doc.sents:
			tot += 1
			# Tokenize and convert to lower case
			tokenized = [word.lower() for word in word_tokenizer.tokenize(sent.text)]
			if sentiment.classify(tokenized) == 'subj': subj += 1
		subjectivities.append(subj/tot)
	return subjectivities

def VaderSentiment(sentences):
	# Input: List of sentences
	# Output: sentiment 0-2 are 0 < sent < 1, 3 is -1 < sent < 1
	sentiments = []
	sentimentAnalyzer = SentimentIntensityAnalyzer()
	for s in sentences:
		#(neg, neu , pos, compound)
		sentiments.append(sentimentAnalyzer.polarity_scores(s))
	return sentiments

def emotionScore(sentences, lexicon):
	# Input: List of sentences
	# Output: emotional scores over 8 emotions on a scale of 0 to 1
	emotions = [0, 0, 0, 0, 0, 0, 0, 0]
	word_count = 0
	for sent in sentences:
		word_count += len(sent)
		for word in sent:
			word = word.lemma_.lower()
			if word in lexicon:
				for k in range(2, 10):
					emotions[k - 2] += lexicon[word][k]
	emotions = [e/word_count for e in emotions]
	return emotions
