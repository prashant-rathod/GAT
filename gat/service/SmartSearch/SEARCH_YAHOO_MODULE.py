#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 09:08:51 2017

@author: ruobingwang
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 21:30:10 2017

@author: ruobingwang
"""

import time
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import re
import requests
from bs4 import BeautifulSoup

class yahooURL(object):
    
    def __init__(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.driver=webdriver.Chrome(os.path.expanduser('./chromedriver'))
        
    def get_urls(self,url):
        driver=self.driver
        driver.get(url)
        elems = driver.find_elements_by_xpath("//a[@href]")
        href=[]
        for elem in elems:
            link=elem.get_attribute("href") 
            try:
                if 'yahoo.com' not in link and 'http' in link and 'search' not in link and 'smashboards.com' not in link:
                    href.append(link)
            except:
                pass
                
        return list(set(href))
        
    
    
    

   
 
    ''' 
    def lookup(self,driver, query):#another way to initiate search, but hard to connect to next part
        driver.get("https://www.google.com/")
        try:
            box = driver.wait.until(EC.presence_of_element_located(
                (By.NAME, "q")))
            button = driver.wait.until(EC.element_to_be_clickable(
                (By.NAME, "btnK")))
            box.send_keys(query)
            button.click()
        except TimeoutException:
            print("Box or Button not found in google.com")
        url=driver.current_url
        return url
    '''
    
    def search_urls(self,keyword,pagenum):
        driver=self.driver
        searchurl=self.lookup(keyword) ### url of first page of google search
        driver.get(searchurl)
        driver.find_element_by_class_name('mag-glass').click()
        time.sleep(5)
        results=self.get_urls(driver.current_url) 
        for i in range(pagenum):
            driver.find_element_by_class_name('next').click()# for chrome
            time.sleep(5) # wait to load page
            current_url=driver.current_url
            results[0:0]=self.get_urls(current_url)
       
        
        driver.quit()
        self.display.stop()
        return results
            
           
            

    

    def lookup(self,query):
        #return 'https://search.yahoo.com/search;_ylt=AwrBT7nXbaBZ07MAby2l87UF;_ylc=X1MDOTU4MTA0NjkEX3IDMgRmcgMEZ3ByaWQDU2pvM0hNTHVUaWVGREo2dS5lR2JaQQRuX3JzbHQDMARuX3N1Z2cDMTAEb3JpZ2luA3NlYXJjaC55YWhvby5jb20EcG9zAzEEcHFzdHIDbm9ydARwcXN0cmwDNARxc3RybAMxMwRxdWVyeQNOb3J0aCUyMEtvcmVhBHRfc3RtcAMxNTAzNjg2MTEx?p='+query+'&fr=sfp&fr2=sa-gp-search&iscqry='
        return 'https://search.yahoo.com/?p='+query
        #partially comes from python package Google-Search-API
        #def normalize_query(query):
        #    return query.strip().replace(":", "%3A").replace("+", "%2B").replace("&", "%26").replace(" ", "+")
        #return "http://www.google.com/search?hl=en&q=%s&start=%i&num=%i" % (normalize_query(query), 0 * 10, 10)

    
if __name__ == "__main__":
    g=yahooURL()
    result=g.search_urls('North Korea threaten unconventional attack',5)
    print(result)
    #driver=g.driver
    #searchurl=g.lookup("North Korea")
   # driver = g.init_driver()
    #driver.get(searchurl)
    #s=g.lookup(g.driver, "Selenium")
    #driver.find_element_by_link_text("Next").click()
    #driver.current_url
    #time.sleep(5)
       
    