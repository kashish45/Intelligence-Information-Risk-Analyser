# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 02:46:42 2021

@author: kusha
"""

import regex as re
import mailSum as ms
import joblib

from mailSum import utilityFunctions

ms = utilityFunctions()


rf = joblib.load('model.pkl') 
vector = joblib.load('tfidf.pkl') 

class modelFunction(object):

    def __init__(self):
        self.model = []

    def modelFunction(self,text):

        self.model = []
        data = re.sub(r'\W', ' ', str(text))
        data = data.lower()
        data = re.sub(r'^br$', ' ', data)
        data = re.sub(r'\s+br\s+',' ',data)
        data = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", data)
        data = re.sub(r'\s+[a-z]\s+', ' ',data)
        data = re.sub(r'^b\s+', '', data)
        data = re.sub(r'\s+', ' ', data)
        self.model.append(data)   
            
            
        X_text = vector.transform(self.model).toarray()   
        
        res = rf.predict(X_text) 
        
        res = ms.listToString(res)
        
        return res


 
    