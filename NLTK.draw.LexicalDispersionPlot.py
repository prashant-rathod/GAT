import nltk, re, pprint
from nltk import word_tokenize

def plot(filename):
	raw = open(filename, encoding = 'utf8').read()
	tokens = word_tokenize(raw)
	text = nltk.Text(tokens)
	text.concordance('Clinton')
	print("Total text length is", len(text))
	print("Total vocabulary length is", len(set(text)))
	print("Average no of times word used is", len(text) / len(set(text)))
	return text.dispersion_plot(['Clinton', 'Women', 'USA', 'ISIS'])