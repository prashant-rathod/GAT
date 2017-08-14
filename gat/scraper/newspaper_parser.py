import newspaper
import nltk

def get_urls(news_site):
	site = newspaper.build(news_site)
	urls = []
	for article in site.articles:
		print(article.url)
		urls.append(article.url)
	for category in site.category_urls():
		print(category)

def parse_article(article):
	article.download()
	article.parse()
	article.nlp()