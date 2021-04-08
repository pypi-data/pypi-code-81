# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 15:44:39 2021

@author: User
"""
import core_helper.helper_general as hg
hg.set_base_path()

import json
import os
import math
import sys

import pandas as pd
import numpy as np
import time
print(np.where(np.array([0.5,0.4,0.7])>0.5, 1, 0))
#import core_helper.helper_plot as hp
import src.Prj_Core.core_helper.helper_plot as hp

#import model.general as g
import src.Prj_Core.core_helper.model.general as g

import src.Prj_Core.core_helper.model.neg_bagging_fraction__lgb_model as nbf_lgb_model
import src.Prj_Core.core_helper.model.scale_pos_weight__lgb_model as spw_lgb_model
import src.Prj_Core.core_helper.model.custom_bagging__lgb_model as cb_lgb_model

#import model.neg_bagging_fraction__lgb_model as nbf_lgb_model
#import model.scale_pos_weight__lgb_model as spw_lgb_model
#import model.custom_bagging__lgb_model as cb_lgb_model

def modelar_clasificacion_binaria(strategy, X_train=None,y_train=None,X_test=None,y_test=None,url=""):
    start = time.time()
    if (strategy=="neg_bagging_fraction__lgb_model"):
        model , predicted_probas   = nbf_lgb_model.modelar(X_train,y_train,X_test,y_test,url)
    if (strategy=="scale_pos_weight__lgb_model"):
        model , predicted_probas   = spw_lgb_model.modelar(X_train,y_train,X_test,y_test,url)
    if (strategy=="custom_bagging__lgb_model"):
        model , predicted_probas   = cb_lgb_model.modelar(X_train,y_train,X_test,y_test,url)

    kpis = generar_reporte(model,predicted_probas,X_test,y_test,url)
    print("Time elapsed: ", time.time() - start)
    
    return model , predicted_probas  , kpis
    

def generar_reporte(model,predicted_probas, X_test, y_test,url):    
    kpis = hp.print_kpis_rendimiento_modelo(y_test,predicted_probas,url)   
    if  isinstance(model, list)==False:
        hp.print_shap_plot(model, X_test, url)      
    g.generate_summary_evaluation(X_test,predicted_probas,y_test,url) 
    return kpis
    
    
def predecir_clasificacion_binaria(model, X=None, umbral=0.5):
    
    if  isinstance(model, list)==False:    
        predicted_probas = model.predict_proba(X)
        y_prob_uno = predicted_probas[:,1]
    else:
        y_pred,y_prob_uno , predicted_probas = cb_lgb_model.predict_proba(model, X)
    
    y_pred_uno = np.where(y_prob_uno >= umbral, 1, 0).tolist()
    
    return y_pred_uno, y_prob_uno , predicted_probas



'''            
def split_x_y(ID_GRADO,macro_region,modalidad="EBR"):

    lista_regiones = get_macro_region(macro_region)
    list_join_n=[]
    list_join_n_mas_1=[]
    for region in lista_regiones:

        url_dir = "{}/{}/".format(region,ID_GRADO)
        print(url_dir)
        try:
            df_join_n , df_join_n_mas_1 = get_saved_join_data(url_dir,modalidad=modalidad)
        except:
            continue
        
        #df_join_n , df_join_n_mas_1 = get_saved_join_data(url_dir,modalidad=modalidad)
        df_join_n['REGION']= region
        df_join_n_mas_1['REGION']= region
        
        ############tempEEE#######
        df_join_n['D_REGION']= region
        df_join_n_mas_1['D_REGION']= region
        ########################
        
        
        print(region)
        print(df_join_n.DESERCION.value_counts())
        list_join_n.append(df_join_n)
        list_join_n_mas_1.append(df_join_n_mas_1)

    df_join_n = pd.concat(list_join_n)
    df_join_n_mas_1 = pd.concat(list_join_n_mas_1)

    fe_df(df_join_n,df_join_n_mas_1)

    X_train, X_test, y_train, y_test , X_t, X_t_eval, y_eval , ID_P_T,ID_P_T_MAS_1, y = tranform_data(df_join_n,df_join_n_mas_1,False)
    

    return X_train, X_test, y_train, y_test , X_t, X_t_eval, y_eval ,  ID_P_T,ID_P_T_MAS_1 , y
   

def get_saved_join_data(url_dir,sub_dir="data",modalidad="EBR"):
    
    if not url_dir:
        url_dir="../02.PreparacionDatos/03.Fusion/reporte_modelo/"+sub_dir+"/"
    else:
        url_dir = '{}/{}'.format("../02.PreparacionDatos/03.Fusion/reporte_modelo/"+sub_dir,url_dir)
        if not os.path.exists(url_dir):
            os.makedirs(url_dir)
        print("reporte generado en : "+url_dir)
    
    if (modalidad=="EBR"):
        specific_url = url_dir+"data.csv"
        specific_url_eval = url_dir+"data_eval.csv"
    else:
        specific_url = url_dir+"data_{}.csv".format(modalidad)
        specific_url_eval = url_dir+"data_eval_{}.csv".format(modalidad)        
    
    dt = {'COD_MOD':str,'COD_MOD_T':str,'ANEXO':int,'ANEXO_T':int,'EDAD':int,
          'N_DOC':str,'COD_MOD_T_MENOS_1':str,
          'ANEXO_T_MENOS_1':int,'NUMERO_DOCUMENTO_APOD':str,'ID_PERSONA':int}

    df=pd.read_csv(specific_url,dtype=dt, encoding="utf-8") 
    df_eval=pd.read_csv(specific_url_eval,dtype=dt, encoding="utf-8") 
    
    return df,df_eval

 ''' 