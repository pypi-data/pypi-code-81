import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer

import random
import nltk
import json
from nltk import sent_tokenize
class Understand():
    def __init__(self,number_of_intent_classes):
        oof = number_of_intent_classes
        if oof/2 == oof//2:
            neighbors = oof+1
        else:
            neighbors = oof
        self.model =  KNeighborsClassifier(n_neighbors=neighbors)
    def fit(self):
        global lolser
        onn = json.load(open('training.json','r'))
        lols = []
        labels =[]
        for item in onn['intentdata']:
            for ntem in item:
                lols.append(ntem)
                labels.append(onn['intentdata'].index(item))
        fn = {'sent': lols, 'label': labels}
        df = pd.DataFrame.from_dict(fn)
        X = df['sent']
        y = df['label']
        nono = list(zip(X, y))
        random.shuffle(nono)
        n, r = zip(*nono)
        X = list(n)
        y = list(r)
        lolser = CountVectorizer().fit(X)
        X = lolser.transform(X)

        self.model.fit(X, y)
    def predict(self,sent_to_predict):
        global lolser
        onn = json.load(open('training.json', 'r'))
        response = sent_to_predict.lower()
        response = lolser.transform([response.lower()])
        response = response[0]
        return onn['intentcategories'][response[0]]









