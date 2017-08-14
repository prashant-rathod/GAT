import pickle
import string
import re
import nltk
from random import shuffle
from nltk import word_tokenize, pos_tag, ne_chunk, ngrams
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import names
from nltk.corpus import treebank
from nltk.corpus import movie_reviews
from nltk.stem.porter import PorterStemmer
from nltk.tag import tnt
from nltk.tag import SennaNERTagger
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import MaxentClassifier
from nltk import NaiveBayesClassifier
from sklearn.externals import joblib

#####################################################
################# Parsing Functions #################
#####################################################

"""
Reads user selected textfile
INPUT: 
	file: file name to be read absolute path if file is outside of the directory with parser.py)
OUTPUT: 
	text: raw text (string)
"""
def readFile(file):
	text = open(file)
	return text
"""
Tokenize Sentences
INPUT: 
	raw: raw text (string)
OUTPUT: 
	sentences: list of sentences (string)
NOTE: NLTK handles tokenizing for 17 languages. 
Follow the spanish example below for loading a tokenizer for a particular language/

>>> spanish_tokenizer = nltk.data.load(‘tokenizers/punkt/spanish.pickle’)
>>> spanish_tokenizer.tokenize(‘Hola amigo. Estoy bien.’)
[‘Hola amigo.’, ‘Estoy bien.’]
"""
def sentenceTokenizer(raw):
	sentences = sent_tokenize(raw)
	return sentences

"""
Tokenize on Stop Words
INPUT: 
	sentence: sentence (string)
	mode: "r" for remove stopwords, "k" for keep stopwords (default: keep)
OUTPUT: 
	words: list of words (string)
"""
def wordTokenizer(sentence, mode = "k"):
	words = word_tokenize(sentence)
	if mode == "r":
		stopWords = set(stopwords.words('english'))
		words = [w for w in words if w not in stopWords]
	return words

"""
Modify words to their stem form using the Porter Algorithm (e.g. "gaming" to "game")
INPUT: 
	words: list of words (string)
OUTPUT: 
	words_stemmed: list of words (string), words that can't be stemmed are left unchanged (e.g. "the")
"""
def wordStemmer(words):
	porter_stemmer = PorterStemmer()
	words = [porter_stemmer.stem(word) for word in words]

"""
Tag parts of speech, uses wordTokenizer function. Use POS_Tag.csv to understand the POS tags
INPUT: 
	sentence: sentence (string)
OUTPUT: 
	pos_words: list of tuples (word, tag) [(string, string)]
"""
def posTagger(sentence):
	words = wordTokenizer(sentence)
	pos_words = nltk.pos_tag(words)
	return pos_words

"""
Following two are alternative options to the posTagger() function above. 

1. sentencePOS_Tagging can tag a group of sentences but is not refined for stopwords. 
	Preferably do it manually with the posTagger() function above
2. trainPOS_tagger trains a tagger using NLTK corpora to tag words. 
	Allows for tagger customization to a specific domain with a curated training set.
"""
def sentencePOS_Tagging(sentences):
    """
    Use NLTK's currently recommended part of speech tagger to tag the
    given list of sentences, each consisting of a list of tokens.
    """
    tagger = load('taggers/maxent_treebank_pos_tagger/english.pickle')
    return tagger.batch_tag(sentences)

def trainPOS_Tagger():
	train_data = treebank.tagged_sents()[:3000]
	test_data = treebank.tagged_sents()[3000:]
	tnt_pos_tagger = tnt.TnT()
	tnt_pos_tagger.train(train_data)
	tnt_pos_tagger.evaluate(test_data)
	f = open('tnt_treebank_pos_tagger.pickle', 'w')
	pickle.dump(tnt_pos_tagger, f)
	f.close()


"""
Chunks a sentence based on individual noun phrases, uses posTagger function
Used for identifying tropes. Needs refinement for phrase identification
INPUT: 
	sentence: sentence (string)
OUTPUT: 
	parse_result: parsed sentence tree with parts of speech tagged
"""
def npChunking(sentence):
	grammar = "NP: {<DT>?<JJ>*<NN>}"
	pos_words = posTagger(sentence)
	chunkParser= nltk.RegexpParser(grammar)
	parse_result = chunkParser.parse(pos_words)
	return parse_result

"""
Chunks a sentence and performs Name Entity Recognition (NER). Uses several parsing helper functions
Used for geolocating (GPE tag refers to location)
Used for object, subject identification
INPUT: 
	sentence: sentence (string)
OUTPUT: 
	ne_chunks: a list of the entities in the sentence (stopwords removed) with their name entity tags 
		(see the main function for an example)
"""
def NEChunker(sentence):
	ne_chunks = ne_chunk(posTagger(sentence))
	return ne_chunks

"""
Performs a recursive traversal of the NEChunker output 
INPUT: 
	t: name entity tree (outputted from NEChunker())
OUTPUT: 
	prints the tree for readability; the output can be parsed for more information, 
		but parsing the tree will be more efficient and fluid
"""
def treeTraverse(t):
    try:
        t.label()
    except AttributeError:
        print(t, end=" ")
    else:
        print('(', t.label(), end=" ")
        for child in t:
            treeTraverse(child)
        print(')', end=" ")

def treeTraverseString(t):
    try:
        t.label()
    except AttributeError:
        return str(t) + " "
    else:
        string = '(' + t.label() + " "
        for child in t:
            string += treeTraverseString(child)
        return string + ')' + " "

"""
Takes the output from the NEChunker() and does IOB tagging 
Used for identifying verbs to match to CAMEO codes 
Used for assistance in identifying tropes. Needs refining
INPUT: 
	sentence: name entity tree (outputted from NEChunker())
OUTPUT: 
	iob_tagged: a list of the words in the sentence inputted into NEChunker() 
		with their parts of speech and sentence structure tagged
		(go to main function for an example)
"""
def IOB_Tagging(t):
	iob_tagged = tree2conlltags(t)
	return iob_tagged

###################################
###### Gender Classification ######
###################################
"""
Note Maximum Entropy Models requires downloading the MEGAM optimization package.
1. Download the source http://www.umiacs.umd.edu/~hal/megam/index.html
2. Download ocaml and opam
3. Compile MEGAM in the downloaded source. Follow the  instructions below for compiling
	a. In the Makefile change line 74 to "WITHCLIBS =-I /usr/local/lib/ocaml/caml"
	b. In the Makefile change line 62 to "WITHSTR =str.cma -cclib -lcamlstr"
	c. run make opt for the faster optimized version; it will produce megam.opt
4. Run the followiwng config_megam() to find the binary version of megam.opt
5. Copy the binary version of megam.opt into the system binary path 
	"sudo cp megam.opt /usr/local/bin" or wherever NLTK is accessing
"""
_megam_bin = "/home/nikita/Projects/GAT/GAT_NLP_JamesWu/NLP/megam_0.92"
def config_megam(bin=None):
    """
    Configure NLTK's interface to the ``megam`` maxent optimization
    package.
 
    :param bin: The full path to the ``megam`` binary.  If not specified,
        then nltk will search the system for a ``megam`` binary; and if
        one is not found, it will raise a ``LookupError`` exception.
    :type bin: str
    """
    global _megam_bin
    _megam_bin = find_binary(
        'megam', bin,
        env_vars=['MEGAM'],
        binary_names=['megam.opt', 'megam', 'megam_686', 'megam_i686.opt'],
        url='http://www.umiacs.umd.edu/~hal/megam/index.html')

"""
Feature Extractor Helper Function for the Gender classifier
INPUT: 
	name: corresponds to the (PERSON) tag that results from the NEChunker() function (string)
OUTPUT: 
	features: relevant features for determining gender of a PERSON {string, char}
"""

def gender_features(name):
    features = {}
    features["fl"] = name[0].lower()
    features["ll"] = name[-1].lower()
    features["fw"] = name[:2].lower()
    features["lw"] = name[-2:].lower()
    return features
"""
Uses NLTK corpora to train a gender classifier model for the PERSON name entity chunk
INPUT: 
	model: the type of model trained, Naive Bayes or Maximum Entropy (follow above guide for installing megam)
OUTPUT: 
	The model is pickled in the same directory as the script and can be accessed with predictGender()
"""

def trainGenderClassifier(model="NB"):
	my_names = ([(name, 'male') for name in names.words('male.txt')] +
		[(name, 'female') for name in names.words('female.txt')])
	shuffle(my_names)
	train_set = [(gender_features(n), g) for (n, g) in my_names]
	if model == "NB":
		nb_classifier = NaiveBayesClassifier.train(train_set)
		joblib.dump(nb_classifier, 'nb_gender_classifier.pkl')
	elif model == "ME": 
		me_classifier = MaxentClassifier.train(train_set, "megam")
		joblib.dump(me_classifier, 'me_gender_classifier.pkl')
	else:
		raise ValueError("Enter Model Type: Naive Bayes (NB) or Maximum Entropy (ME)")

"""
Uses picked gender classifier model to predict a gender for a test name
INPUT: 
	name: name (string)
	model: type of model you want to use (NB faster, ME slower and more accurate for larger corpora)
OUTPUT: 
	predicts: prediction (male or female)
	male_prob: probability of male (if close to 0.5, the name may not be a PERSON NE)
	female_prob: probability of female (if close to 0.5, the name may not be a PERSON NE)
"""
def predictGender(name, model="NB"):
	test = gender_features(name)
	classifier = None
	if model == "ME":
		classifier = joblib.load("me_gender_classifier.pkl") 
	elif model == "NB":
		classifier = joblib.load("nb_gender_classifier.pkl") 
	predicts = classifier.classify(classifier, test)
	male_prob = classifier.prob("m")
	female_prob = classifier.prob("f")
	return predicts,male_prob,female_prob

#######################################
######### Sentiment Analysis ##########
#######################################
"""
Feature Generator Helper Function for the Sentiment classifier, uses ngrams and bag of words technique
INPUT: 
	words: all of the words in the document (document can be a sentence, article, essay, etc)
OUTPUT: 
	all_features: relevant features for determining sentiment of the document
"""

def sentiment_features(words, n=2):
	all_features = bag_of_words(words)
	ngram_features = bag_of_ngrams(words, n=n)
	all_features.update(ngram_features)   
	return all_features
"""
Helper functions for sentiment_features 
"""
def bag_of_words(words):
	return dict([(word, True) for word in words])

def bag_of_ngrams(words, n=2):
	ngs = [ng for ng in iter(ngrams(words, n))]
	return bag_of_words(ngs)

"""
Uses NLTK corpora to train a sentiment classifier model
OUTPUT: 
	The model is pickled in the same directory as the script and can be accessed with predictSentiment()
"""
def trainSentimentClassifier():
	documents = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
	shuffle(documents)
	train_set = [(sentiment_features(d), c) for (d, c) in documents]
	#me_classifier = MaxentClassifier.train(train_set, "megam")
	nb_classifier = NaiveBayesClassifier.train(train_set)
	joblib.dump(nb_classifier, "nb_sentiment_classifier.pkl")
"""
Uses pickled sentiment classifier model to predict a sentiment for a text
INPUT: 
	text: raw text (string)
OUTPUT: 
	sentiment_probabilities: prediction (positive or negative)
	positive_prob: probability of positive sentiment (closer to 0.5 may show weaker sentiment)
	negative_prob: probability of negative sentiment (closer to 0.5 may show weaker sentiment)
	most_useful: most useful words in the text for determining the sentiment
"""
def predictSentiment(text):
	test = sentiment_features(wordTokenizer(text, "r"))
	me_classifier = joblib.load("nb_sentiment_classifier.pkl")
	sentiment = me_classifier.classify(test)
	sentiment_probabilities = me_classifier.prob_classify(test)
	positive_prob = sentiment_probabilities.prob("pos")
	negative_prob = sentiment_probabilities.prob("neg")
	most_useful = me_classifier.most_informative_features(5)
	return sentiment,positive_prob,negative_prob,most_useful

if __name__=="__main__":
	tags = npChunking("All work and no play makes jack dull boy. this is a test for stop words.")
	treeTraverse(tags)
	""" Output below
	( S ( NP ('All', 'DT') ('work', 'NN') ) ('and', 'CC') ( NP ('no', 'DT') ('play', 'NN') ) ('makes', 'VBZ') ( NP ('jack', 'NN') ) ( NP ('dull', 'JJ') ('boy', 'NN') ) ('.', '.') ('this', 'DT') ('is', 'VBZ') ( NP ('a', 'DT') ('test', 'NN') ) ('for', 'IN') ( NP ('stop', 'NN') ) ('words', 'NNS') ('.', '.') )
	"""
	ne_tree = NEChunker("Mark and John are working at Google in San Francisco.")
	treeTraverse(ne_tree)
	"""Output below
	( S ( PERSON ('Mark', 'NNP') ) ('and', 'CC') ( PERSON ('John', 'NNP') ) ('are', 'VBP') ('working', 'VBG') ('at', 'IN') ( ORGANIZATION ('Google', 'NNP') ) ('in', 'IN') ( GPE ('San', 'NNP') ('Francisco', 'NNP') ) ('.', '.') )
	"""
	print(IOB_Tagging(ne_tree))
	"""Output below
	[('Mark', 'NNP', 'B-PERSON'), ('John', 'NNP', 'B-PERSON'), ('working', 'VBG', 'O'), ('Google', 'NNP', 'B-PERSON'), ('San', 'NNP', 'I-PERSON'), ('Francisco', 'NNP', 'I-PERSON'), ('.', '.', 'O')]
	"""
	
