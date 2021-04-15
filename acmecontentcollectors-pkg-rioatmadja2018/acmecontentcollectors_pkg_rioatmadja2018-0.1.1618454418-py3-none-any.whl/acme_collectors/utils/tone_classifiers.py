#!/usr/bin/env python
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer 
import joblib 
from nltk import sent_tokenize 
import os 
import pandas as pd 
from acme_collectors.utils.constants import PKL_CLF, TONES 

from typing import Dict, List
from pandas.core.frame import DataFrame
"""
Name: Rio Atmadja
Date: January 08,2020 
Description: tone classifier utilities 
"""

def classify_tones(text, clf_path: str = PKL_CLF) -> List[Dict] :
    """
    Description 
    ------------

    Parameters
    -----------
    :text: given a non-empty text 

    Return
    ------
    :return: a dictionary with analytical, joy, sadness, fear, confident, anger, and tentative attributes 
    """ 
    if not text: 
        raise ValueError(f"You must provide a non-empty text.")

    if not os.path.exists(clf_path): 
        raise FileNotFoundError(f"Unable to find the following file : {PKL_CLF}. Please check for this file. {os.getcwd()}")

    # unpack pickle classifier here 
    pkl = joblib.load(clf_path)
    clf, tfidf, vect = tuple(pkl.values())

    mapped_tones: Dict = dict(zip(range(7), TONES))
    results: List = []
    for index, word in enumerate(sent_tokenize(text),1):
        sentence_tone: str = mapped_tones.get(clf.predict(tfidf.transform(vect.transform([word]))).tolist()[0]) 
        tone_proba_score: DataFrame = pd.DataFrame(clf.predict_proba(tfidf.transform(vect.transform([word]))), 
                                               columns=TONES, 
                                               index=['Sentence']).transpose().sort_values(by='Sentence', ascending=False)

        results.append({'sentence': word,
                        'tone': sentence_tone,
                        'score': tone_proba_score.iloc[0][0] 
                       })
    return results
