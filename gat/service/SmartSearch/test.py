from gat.service.SmartSearch.SEARCH_BING_MODULE import bingURL
from gat.service.SmartSearch.SVO_SENT_MODULE_spacy import SVOSENT
import gat.service.SmartSearch.SCRAPER as SCRAPER
import time

Subject = 'North Korean'
CAMEO = 'threaten unconventional attack'
Object = ''
sentence = Subject + ' ' + CAMEO + ' ' + Object  # subject+cameo code

bing = bingURL()
t0 = time.time()
urls = bing.search_urls(sentence, 3)
t1 = time.time()
print('time cost:', t1 - t0)
print('#urls found:', len(urls))


articles = SCRAPER.scrape_from_urls(urls)

svo_sent = SVOSENT()
articles_list = svo_sent.split_and_clean(articles)
result = svo_sent.batchProcessArticles(articles_list)

print(result)
