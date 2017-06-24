from tika import parser
from textblob import TextBlob

def return_text(text):
    return (text)

def runPA(filename):
	text = parser.from_file(filename)
	x = str(return_text(text))
	text = TextBlob(x)
	return text.sentiment