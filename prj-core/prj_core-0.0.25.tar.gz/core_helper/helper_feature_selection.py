# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 08:46:06 2021

@author: User
"""
import pandas as pd
import numpy as np

def drop_cls_unique_value(df):
    for col in df.columns:
        if len(df[col].unique()) == 1:
            print ("dop column : ",col)
            df.drop(col,inplace=True,axis=1)
    return df

def drop_corr_columns(X_t):
    cor_matrix = X_t.corr().abs()
    upper_tri = cor_matrix.where(np.triu(np.ones(cor_matrix.shape),k=1).astype(np.bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)]
    print("Eliminando columnas CORR")
    print(to_drop)
    X_t.drop(to_drop, inplace=True, axis=1)
    return X_t


def drop_nan_columns(X_t,p_min_val = .01):
    temp1 = X_t.columns    
    thresh = len(X_t) * p_min_val
    X_t.dropna(thresh = thresh, axis = 1, inplace = True)
    temp2 = X_t.columns     
    l = list(set(temp1) - set(temp2))
    print("Columnas eliminadas por missing",p_min_val)
    print(l)
    return X_t
