# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 00:36:06 2021

@author: User
"""
import pandas as pd
import numpy as np
import src.Prj_Core.core_helper.helper_acces_db as hadb
import src.Prj_Core.core_helper.helper_clean as hc

def agregar_sisfoh(df,df_sisfoh=None):    
    
    if df_sisfoh is None:
        df_sisfoh = hadb.get_sisfoh()  
    
    if 'NUMERO_DOCUMENTO_APOD' not in df.columns:
        print("ERROR: No existe la columnna NUMERO_DOCUMENTO_APOD en el DF proporcionado")
        
    df['NUMERO_DOCUMENTO_APOD'] = df['NUMERO_DOCUMENTO_APOD'].str.replace('.0', '')
    df['NUMERO_DOCUMENTO_APOD']=df['NUMERO_DOCUMENTO_APOD'].apply(lambda x: '{0:0>8}'.format(x))
    df['NUMERO_DOCUMENTO_APOD'] = df['NUMERO_DOCUMENTO_APOD'].str.replace('00000nan', '00000000')     
    
    df = pd.merge(df, df_sisfoh, left_on=["NUMERO_DOCUMENTO_APOD"], right_on=["PERSONA_NRO_DOC"],  how='left')
    df = hc.fill_nan_with_nan_category_in_cls(df , ["SISFOH_CSE"])

    del df["PERSONA_NRO_DOC"]
    
    return df


