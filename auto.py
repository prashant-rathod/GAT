
import json
import collections
import tensorflow
import sys
import os


f1=open("/Users/Moussa/documents/input.txt", "r")
contents =f1.readlines()
f1.close
result = contents
#this is the text file from web scraping
f= open("/Users/Moussa/documents/text_test.txt","w")
for i in result:
    f.write(i)
f.close
f2=open("/Users/Moussa/documents/text_test.txt", "r")
for i in result:
    print(i)
f2.close
os.system('syntaxnet/demo.sh --input=MAIN-IN —output =MAIN-OUT')
os.system('syntaxnet/demo.sh --input=MAIN-IN —output =MAIN-OUT')
