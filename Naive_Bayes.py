from tika import parser
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def return_text(text):
    return (text)

def runNB(filename):
	if filename == '':
		return None
	text = parser.from_file(filename)

	text = str(return_text(text))

	blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
	return blob.sentiment

#print(runNB('trumpspeech.pdf'))