from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,log_loss
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
import spacy
from gat.dao import dao

def accuracy(y_true,y_pred):
    correct=0
    for i in range(len(y_true)):
        if (list(y_true)[i]==list(y_pred)[i]).all():
            correct=correct+1
    return correct*1.0/len(y_true)

def Encode(x):
    result=[]
    for e in list(x):
        result.append(list(e).index(1))
    return result

def Decode(x):
    result=[]
    for e in x:
        r=[0]*len(set(x))
        r[e]=1
        result.append(r)
    return result
        
def top5index(a):
    return sorted(range(len(a)), key=lambda i: a[i])[-5:]
    
def top5pred(pred_ba):
    result=[]
    for e in pred_ba:
        top5=top5index(e)
        result.append(top5)
    return result

def top5accuracy(y_true, y_pred):
    correct=0
    for i in range(len(y_true)):
        if y_true[i] in y_pred[i]:
            correct=correct+1
    return correct*1.0/len(y_true)
                    



model=joblib.load('gat/CameoPrediction/model.pkl')
vector_rule=pd.read_csv('gat/CameoPrediction/vectorize_rules.txt', sep='	',header=None)
cameo_book=pd.read_csv('gat/CameoPrediction/CAMEO_code_new.csv')
top_words=list(pd.read_csv('gat/CameoPrediction/top_all_words_from_analysis.txt',sep='	',header=None).head(3000)[0])

nlp=dao.spacy_load_en()

def top5CAMEO(sentence):
    phrase=[e.lemma_ for e in nlp(sentence)]
    sentence_binary=np.zeros(3000,dtype=int)
    
    for i in range(len(top_words)):
        if top_words[i] in phrase:
            sentence_binary[i]=1
    sentence_binary=sentence_binary.reshape(1,-1)
    pred_ba=model.predict_proba(sentence_binary)
    pred_top5=top5pred(pred_ba)[0]
    cameo_top5=list(vector_rule[vector_rule[1].isin(pred_top5)][0])
    cameo_5=list(cameo_book[cameo_book['Code'].isin(cameo_top5)]['Move'])
    return cameo_5


