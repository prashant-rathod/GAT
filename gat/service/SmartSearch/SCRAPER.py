#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 10:03:03 2017

@author: ruobingwang
"""

from newspaper import Article
import time
'''
class Downloader(threading.Thread)

def __init__():
    self.current_output = ""


from inside of controller, you have a method
downloader = Downloader()

@...route("/update_progress")
def getCurrentOutput():
    return json(downloader.current_output)

in javascript, have a function that pings
function update(){
    $.ajax("/update_progress") // check the rest of the syntax
}
'''

# temporay function to scrap article,modified from James's code

def url_reader(url):
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
    print("The article: {} is downloaded and parsed".format(title))
    return title, authors, date, text  # keywords , summary


def to_string(title, authors, date, text):  # mimic corpus style
    article = 'Title:' + title + '(title_end)' + 'Full text:' + text + 'Publication date - ' + str(
        date) + '____________________________________________________________'
    return article


def scrape_from_urls(urls):  # urls is list of string, each string is a url
    articles = ''
    t0 = time.time()
    for url in urls:
        try:
            title, authors, date, text = url_reader(url)
            articles = articles + to_string(title, authors, date, text)
        except:
            print('dowload failed')
    t1 = time.time()
    print('cost time:', t1 - t0)
    return articles


if __name__ == "__main__":
    urls = [
        'https://www.nytimes.com/2017/09/22/world/asia/kim-trump-north-korea.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news',
        'https://www.nytimes.com/2017/08/09/world/asia/north-korea-missiles-guam.html?action=click&contentCollection=Asia%20Pacific&module=RelatedCoverage&region=Marginalia&pgtype=article']

    articles = scrape_from_urls(urls)
    print(articles)
