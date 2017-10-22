#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import http.cookiejar
import json
import urllib.request, urllib.error, urllib.parse
from selenium import webdriver
from pyvirtualdisplay import Display

class BingScraper(object):

    def __init__(self, query, num_images, DIR = "Pictures"):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.query = query
        self.num_images = num_images
        self.DIR = DIR

    def get_soup(url,header):
        #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),
        # 'html.parser')
        return BeautifulSoup(urllib.request.urlopen(
            urllib.request.Request(url,headers=header)),
            'html.parser')
    def download_images(self):
        query= self.query.split()
        query='+'.join(query)
        url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        driver=webdriver.Chrome(os.path.expanduser('chromedriver'))
        driver.get(url)
        pageSource = driver.page_source

        ActualImages=[]# contains the link for Large original images, type of  image
        if self.num_images > 750:
            raise ValueError("Bing won't allow for more than about 750 images. Going over results in nothing being downloaded")
        while(len(ActualImages)<self.num_images):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            pageSource = driver.page_source
            soup = BeautifulSoup(pageSource, 'lxml')
            try:
                if(driver.find_element_by_class_name("btn_seemore") is not None):
                    driver.find_element_by_class_name("btn_seemore").click()
            except:
                pass
            for a in soup.find_all("a",{"class":"iusc"}):
                #print a
                mad = json.loads(a["mad"])
                turl = mad["turl"]
                m = json.loads(a["m"])
                murl = m["murl"]

                image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
                if((image_name,turl,murl) not in ActualImages and len(ActualImages)<self.num_images):
                    ActualImages.append((image_name, turl, murl))

        print("there are total" , len(ActualImages),"images")

        if not os.path.exists(self.DIR):
            os.mkdir(self.DIR)

        DIR = os.path.join(self.DIR, query.split()[0])
        if not os.path.exists(DIR):
            os.mkdir(DIR)

        ##print images
        for i, (image_name, turl, murl) in enumerate(ActualImages):
            try:
                #req = urllib2.Request(turl, headers={'User-Agent' : header})
                #raw_img = urllib2.urlopen(req).read()
                #req = urllib.request.Request(turl, headers={'User-Agent' : header})
                print(murl)
                raw_img = urllib.request.urlopen(turl).read()

                f = open(os.path.join(DIR, image_name), 'wb')
                f.write(raw_img)
                f.close()
            except Exception as e:
                print("could not load : " + image_name)
                print(e)
        driver.quit()
        self.display.stop()