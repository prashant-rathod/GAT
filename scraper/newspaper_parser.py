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


if __name__ == "__main__":
	urls = get_urls("http://abcnews.go.com/")
	print (urls)