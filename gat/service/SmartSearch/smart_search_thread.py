import threading
import time
from newspaper import Article
from gat.service.SmartSearch.SEARCH_BING_MODULE import bingURL
from gat.service.SmartSearch.SVO_SENT_MODULE_spacy import SVOSENT
import gat.service.SmartSearch.SCRAPER as SCRAPER


class SmartSearchThread(threading.Thread):
    messages = []
    messages_lock = threading.Lock()
    result = None
    result_lock = threading.Lock()

    def __url_reader(self, url):
        article = Article(url)
        article.download()
        article.parse()
        title = article.title
        authors = article.authors
        date = article.publish_date
        text = article.text
        # can also include things like article images, and attached videos
        # article.nlp()
        # keywords = article.keywords
        # summary = article.summary
        self.messages_lock.acquire()
        self.messages.append("The article: {} is downloaded and parsed".format(title))
        self.messages_lock.release()
        return title, authors, date, text  # keywords , summary

    @classmethod
    def __to_string(cls, title, authors, date, text):  # mimic corpus style
        article = 'Title:' + title + '(title_end)' + 'Full text:' + text + 'Publication date - ' + str(
            date) + '____________________________________________________________'
        return article

    def __scrape_from_urls(self, urls):  # urls is list of string, each string is a url
        articles = ''
        t0 = time.time()
        for url in urls:
            try:
                title, authors, date, text = self.__url_reader(url)
                articles += self.__to_string(title, authors, date, text)
            except:
                self.messages_lock.acquire()
                self.messages.append('download failed')
                self.messages_lock.release()
        t1 = time.time()
        self.messages_lock.acquire()
        self.messages.append('cost time:' + str(t1 - t0))
        self.messages_lock.release()
        return articles

    def run(self, sentence=''):
        if sentence:
            self.messages_lock.acquire()
            self.messages.append('Smart Search started.')
            self.messages_lock.release()
            bing = bingURL()
            t0 = time.time()
            urls = bing.search_urls(sentence, 3)
            t1 = time.time()
            self.messages_lock.acquire()
            self.messages.append('time cost:' + str(t1 - t0))
            self.messages.append('#urls found:' + str(len(urls)))
            self.messages_lock.release()
            articles = SCRAPER.scrape_from_urls(urls)
            svo_sent = SVOSENT()
            articles_list = svo_sent.split_and_clean(articles)
            self.result_lock.acquire()
            self.result = svo_sent.batchProcessArticles(articles_list)
            self.result_lock.release()

