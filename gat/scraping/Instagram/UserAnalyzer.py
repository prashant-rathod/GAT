from Spacy_SVO import SVOSENT
from ig import IGscrape
import subprocess
import pandas as pd
import os
import datetime

svo_sent = SVOSENT()

username = 'oliviamunn'

test = IGscrape("m0oseg0ose", "Kasbah5432!")
test.downloadAllMedia(username)

filepath = os.getcwd()+'/'+username+'/'+username+'.json'
metadata = pd.read_json(filepath)
urls = metadata.loc[:, 'urls']
caption = metadata.loc[:, 'caption']
scraped = pd.DataFrame(columns = ['User', 'Caption' , 'Time (UTC)', 'Sentiment', 'Names', 'Dates', 'Locations' , 'URL', 'Filename'])

for i,user in enumerate(caption):
    if user is not None and user['from'] is not None and user['from']['username'] is not None:
        scraped.loc[i, 'User'] =  user['from']['username']
    else:
        scraped.loc[i, 'User'] = ' '

for i,caption_text in enumerate(caption):
    if caption_text is not None and caption_text['text'] is not None:
        scraped.loc[i,'Caption'] = caption_text['text']
        svo = svo_sent.get_svo(caption_text['text'])
        scraped.loc[i, 'Names'] = svo['Names']
        scraped.loc[i, 'Locations'] = svo['Locations']
        scraped.loc[i, 'Dates'] = svo['Event_date']
        sentiment = svo_sent.sentimentAnalysis(caption_text['text'])
        sentiment.pop('Sentence')
        scraped.loc[i, 'Sentiment'] = str(sentiment)
    else:
        scraped.loc[i,'Caption'] = ' '

for i, time in enumerate(caption):
    if time is not None and time['created_time'] is not None:
        scraped.loc[i, 'Time (UTC)'] = datetime.datetime.utcfromtimestamp(int(time['created_time'])).strftime('%Y-%m-%d %H:%M:%S')
    else:
        scraped.loc[i, 'Time (UTC)'] = ' '

for i,url in enumerate(urls):
    url = url[0]
    scraped.loc[i,'URL'] = url
    scraped.loc[i,'Filename'] = url[url.rfind('/')+1 :]

scraped.to_clipboard()