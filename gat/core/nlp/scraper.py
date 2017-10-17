######################################################
################# Scraping Functions #################
######################################################

from newspaper import Article

"""
Reads an article's raw data given an URL
INPUT: 
	url: url of the article to be scraped (string)
OUTPUT:
	title, authors, date, text: information gathered from the article (tuple of strings)
"""
def urlReader(url):
	article = Article(url)
	article.download()
	article.parse()
	title = article.title
	authors = article.authors
	date = article.publish_date
	text = article.text
	source = article.source_url

	print ("The article: {} is downloaded and parsed".format(title))
	return url, title, authors, date, text, source
"""
Writes the gathered information to a uniform text file, includes metadata
INPUT:
	title, authors, date, text: parsed information from urlReader (default string of tuples)
OUTPUT: 
	written text file (format: {title}.txt)
"""
def textWriter(url, title = "No Title Parsed", authors = "No Authors Parsed", date = "No Date Parsed", text = "No Text Parsed"):
	def newline():
		f.write("\n")
	print ("Writing Text File")
	f = open(reformatTitle(title) + ".txt", "w")
	f.write(url + "\n")
	f.write(title + "\n")
	newline()
	for author in authors:
		f.write(author + "\n")
	newline()
	f.write(reformatDate(date) + "\n")
	newline()
	for sentence in separateText(text):
		f.write(sentence + "\n")
	newline()
	f.close()
	print ("Text Written \n")

"""
Function to combine the scraping and writing process
INPUT:
	urls: list of urls (strings)
OUTPUT: 
	articles: list of lists of url's metadata and text
"""
def parseURLs(urls):
	articles = []
	for url in urls:
		title, authors, date, text = urlReader(url)
		articles.append([title, authors, date, text])
		textWriter(url, title, authors, date, text)
	return articles

"""
Helper functions for textWriter
	separateText: parses the raw text into sentences
	preserveOrderDuplicateRemove: removes parsed duplicates in the sentences
	reformatDate: converts date to a more readable form
	reformatTitle: prepares title for naming outputted file
"""
def separateText (text):
	punctuation = ".?!"
	sentences = []
	sentence = ""
	for ch in text:
		sentence += ch
		if ch in punctuation:
			sentences.append(sentence)
			sentence = ""
	sentences = preserveOrderDuplicateRemove(sentences)
	return sentences

def preserveOrderDuplicateRemove(sentences):
    seen = set()
    seen_add = seen.add
    return [x for x in sentences if not (x in seen or seen_add(x))]

def reformatDate(datetime):
	if datetime == None:
		return "No Date Parsed"
	months =   {"01": "January", "02": "February", "03": "March", "04": "April", 
				"05": "May", "06": "June", "07": "July", "08": "August", 
				"09": "September", "10": "October", "11": "November", "12": "December"}
	date = ""
	t = datetime.strftime('%m/%d/%Y')
	parts = t.split("/")
	date += parts[1] + " "
	date += months.get(parts[0]) + " "
	date += parts[2]
	return date

def reformatTitle(title):
	new_title = ""
	for ch in title:
		if ch == " ":
			new_title += "_"
		else:
			new_title += ch
	return new_title
