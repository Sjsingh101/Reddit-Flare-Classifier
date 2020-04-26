#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 10:55:13 2020

@author: sjsingh
"""
import pickle
import praw
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
flares = ['Non-Political',
 'Photography',
 'Science/Technology',
 'CAA-NRC-NPR',
 'Business/Finance',
 'Coronavirus',
 'Sports',
 'Politics',
 'Food',
 'AskIndia',
 'Scheduled',
 'Policy/Economy']

def getdatafromURL(postURL):
    reddit = praw.Reddit(client_id='aAcZ6aykDcIyaw',
                     client_secret='Y-zrtAoc0akVR-qf6SwEGcA0f2A',
                     user_agent='subred-data')
    submission = reddit.submission(url=postURL)
    
    feature={'title':submission.title,
             'score':submission.score,
             'over_18':submission.over_18,
             'awards':len(submission.all_awardings),
             'creation_time':submission.created_utc,
             'selftext':submission.selftext,
             
             }
    return feature

def preprocess_all(urls):
    corpous = []
    over_18 = []
    score = []
    
    for url in urls:    
        post = getdatafromURL(url)
        corpous.append(post['title']+post['selftext'])
        over_18.append(float(post['over_18']))
        score.append(post['score']/mean_score)

    with open("vocab.obj",'rb') as file:
        count_vectorizer = pickle.load(file)
    frequency = count_vectorizer.transform(corpous)
    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(frequency)        
    feature_text = tfidf.transform((frequency)).todense()    
    
    feature_num = np.c_[over_18,score]
    feature_final = np.c_[feature_num,feature_text]
    return feature_final
    

def predict_all(urls):
    urls_clean = [url.replace('\n','') for url in urls]   
    X_test = preprocess_all(urls)
    model={}
    with open("model.obj",'rb') as file1:
        model = pickle.load(file1)
    pred=model.predict(X_test)
    flare_list = [flares[int(i)] for i in pred]
    return dict(zip(urls_clean,flare_list))


mean_score = 1337.46  
def preprocess(url):
    post = getdatafromURL(url)
    titles = [post['title']+post['selftext'],]
    count_vectorizer = {}
    with open("vocab.obj",'rb') as file:
        count_vectorizer = pickle.load(file)
    frequency = count_vectorizer.transform(titles)
    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(frequency)
    feature_text = tfidf.transform((frequency)).todense()
    feature_final = np.c_[float(post['over_18']),float(post['score']/mean_score),feature_text]
    return feature_final
      
def predict(url):
    X_test = preprocess(url)
    model={}
    with open("model.obj",'rb') as file:
        model = pickle.load(file)
    pred=model.predict(X_test)

    return flares[int(pred)]

