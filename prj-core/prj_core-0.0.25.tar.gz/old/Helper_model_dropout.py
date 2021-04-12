import time
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import urllib.request
from simpledbf import Dbf5
import itertools
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import pipeline
import lightgbm as lgb ## cambias

from sklearn.preprocessing import StandardScaler, LabelEncoder , LabelBinarizer
from simpledbf import Dbf5
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform
from helper_transformers import CatTransformer


def get_pipeline():

    lgb_pipe = pipeline.Pipeline([
        #
        #  metric="None", first_metric_only=True -> ignora binary_logloss en early_stopping_rounds
        ('clf', lgb.LGBMClassifier(metric="None", first_metric_only=True, importance_type="gain",n_jobs=4))
        ])


    lgb_param_random = {
        'clf__use_missing':[True],
        'clf__zero_as_missing':[False],
        
        'clf__learning_rate': [0.015,0.012,0.025,0.01,0.0085,0.007,0.005],
        'clf__objective':['binary'],
        #'clf__max_depth': [2,3,5,12,22,30,50,63],
        'clf__max_depth': [-1], 
        
        #'clf__n_estimators': [150,180,200,250,275,300,350,400,450,500,550,600,650,700,750,800,850,900],
        'clf__n_estimators': [70000],
        
        'clf__num_leaves': list(range(7, 50)),  
        'clf__min_data_in_leaf': sp_randint(100, 500),  
        #'clf__min_sum_hessian_in_leaf': [1e-5, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4],
        #'clf__min_data_in_leaf': [50,60,70,80,90,100,110], 
        #'clf__max_bin': [25],        
                              
        'clf__boosting_type': ['gbdt'],
        #'clf__reg_lambda': [0.01, 0.1, 1],
        'clf__reg_alpha': [0, 1e-1, 1, 2, 5, 7, 10, 50, 100],
        'clf__reg_lambda': [0, 1e-1, 1, 5, 10, 20, 50, 100],
        
        #'clf__scale_pos_weight':scale, 
        'clf__feature_fraction':sp_uniform(loc=0.4, scale=0.6),
        'clf__bagging_fraction':sp_uniform(loc=0.2, scale=0.8), 
        #'clf__bagging_fraction':[0.3,0.4,0.5,0.75,0.85,0.9,0.95],
        #'clf__bagging_freq':[2,5,10,15,20,25]# debe ser superior a 0 y menos a 1 para activar bagging_fraction       
        'clf__bagging_freq':[1]# debe ser superior a 0 y menos a 1 para activar bagging_fraction       
        
    }

    return lgb_pipe, lgb_param_random

def tranform_data(df_join,df_join_eval,desercion_eval):
    
    df_join['EDAD_EN_DECIMALES_T']  = df_join['EDAD_EN_DECIMALES_T'].round()
    df_join_eval['EDAD_EN_DECIMALES_T']  = df_join_eval['EDAD_EN_DECIMALES_T'].round()
    
    '''
    df_join['Z_NOTA_MAT_T_MENOS_1']  = df_join['Z_NOTA_MAT_T_MENOS_1'].round()
    df_join['Z_NOTA_OTROS_T_MENOS_1']  = df_join['Z_NOTA_OTROS_T_MENOS_1'].round()
    df_join['Z_NOTA_COM_T_MENOS_1']  = df_join['Z_NOTA_COM_T_MENOS_1'].round()
    df_join['COST_APAFA_T_MENOS_1']  = df_join['COST_APAFA_T_MENOS_1'].round()
    df_join['STD_TRASLADOS']  = df_join['STD_TRASLADOS'].round()       
    
    df_join_eval['Z_NOTA_MAT_T_MENOS_1']  = df_join_eval['Z_NOTA_MAT_T_MENOS_1'].round()
    df_join_eval['Z_NOTA_OTROS_T_MENOS_1']  = df_join_eval['Z_NOTA_OTROS_T_MENOS_1'].round()
    df_join_eval['Z_NOTA_COM_T_MENOS_1']  = df_join_eval['Z_NOTA_COM_T_MENOS_1'].round()
    df_join_eval['COST_APAFA_T_MENOS_1']  = df_join_eval['COST_APAFA_T_MENOS_1'].round()
    df_join_eval['STD_TRASLADOS']  = df_join_eval['STD_TRASLADOS'].round()
    '''
               
            
    column_y = 'DESERCION'
    columns_with_nan = ["JUSTIFICACION_RETIRO_T_MENOS_1","DSC_PAIS","DSC_LENGUA"]#'LENGUA_APOD','ID_PERSONA',
    columns_to_drop = ['COD_MOD_T','ANEXO_T','COD_MOD_T_MENOS_1','ANEXO_T_MENOS_1','ID_GRADO_T_MENOS_1',
                       'NUMERO_DOCUMENTO_APOD','N_DOC','NIVEL_INSTRUCCION_APOD',
                       #'ID_NIVEL','JUSTIFICACION_RETIRO_N_MENOS_1', 
                       #,'NIVEL_INSTRUCCION_APOD_SHORT','ANIOS_ESCOLARIDAD_APOD',
                       #'ID_GRADO_N_MENOS_1','TIPO_DOC','N_DOC',
                       'NOTA_MATEMATICA_X_ALUMNO','NOTA_COMUNICACION_X_ALUMNO','MEAN_NOTA_MATEMATICA_X_CODMOD_NVL_GR',
                       'NOTA_OTROS_X_ALUMNO',
                       'MEAN_NOTA_COMUNICACION_X_CODMOD_NVL_GR','STD_NOTA_MATEMATICA_X_CODMOD_NVL_GR',
                       'STD_NOTA_COMUNICACION_X_CODMOD_NVL_GR',
                       'MEAN_NOTA_OTROS_X_CODMOD_NVL_GR','STD_NOTA_OTROS_X_CODMOD_NVL_GR',#'NOTA_OTROS_X_ALUMNO',
                      ] #,
    cat_muy_largas = ['D_REGION']

    columns_to_drop_all = columns_with_nan+columns_to_drop +cat_muy_largas+[column_y]

    y = df_join[column_y] #DESERCION_2016_2018, DESERCION_2016_2017_2018 DESERCION_2016_2017

    y_eval = None
    if desercion_eval:
        y_eval = df_join_eval[column_y]
        columns_to_drop_all_eval = columns_to_drop_all
    else:
        columns_to_drop_all_eval = columns_with_nan+columns_to_drop +cat_muy_largas




    X = df_join.drop(columns = columns_to_drop_all) 
    ID_PERSONA_EVAL = df_join_eval.ID_PERSONA
    X_eval = df_join_eval.drop(columns = columns_to_drop_all_eval) 


    #X['PALOMITA'] = np.random.randint(1,100, X.shape[0])
    #X_eval['PALOMITA'] = np.random.randint(1,100, X_eval.shape[0])

    ct = CatTransformer(preprocessing="lb")#lb le
    ct.fit(X)
    X_t = ct.transform(X)

    ct = CatTransformer(preprocessing="lb")#lb le
    ct.fit(X_eval)
    X_t_eval = ct.transform(X_eval)

    X_t.drop(['SISFOH_CSE_OTROS'], axis = 1,inplace=True) 
    X_t_eval.drop(['SISFOH_CSE_OTROS'], axis = 1,inplace=True) 
      
    X_t = reduce_mem_usage(X_t)    
    X_train, X_test, y_train, y_test = train_test_split(X_t, y, test_size=0.20,stratify=y,random_state=42)
    
    #X_train['PALOMITA'] = np.random.randn(X_train.shape[0])
    #X_test['PALOMITA'] = np.random.randn(X_test.shape[0])
    
    return X_train, X_test, y_train, y_test , X_t_eval, y_eval,ID_PERSONA_EVAL








def get_summary_evaluation(X,estimator_random,y,url_dir):

    X_eval = X.copy()
    X_eval['PREDICT_PROBA'] = estimator_random.predict_proba(X)[:,1]
    X_eval['PREDICT'] = estimator_random.predict(X)
    if y is not None:
        X_eval['REAL'] =  y

    criteria = [X_eval['PREDICT_PROBA'].between(0,0.1),
                X_eval['PREDICT_PROBA'].between(0.1, 0.2), 
                X_eval['PREDICT_PROBA'].between(0.2, 0.3),
                X_eval['PREDICT_PROBA'].between(0.3, 0.4),
                X_eval['PREDICT_PROBA'].between(0.4, 0.5),
                X_eval['PREDICT_PROBA'].between(0.5, 0.6),
                X_eval['PREDICT_PROBA'].between(0.6, 0.7),
                X_eval['PREDICT_PROBA'].between(0.7, 0.8),
                X_eval['PREDICT_PROBA'].between(0.8, 0.9),
                X_eval['PREDICT_PROBA'].between(0.9,0.95),
                X_eval['PREDICT_PROBA'].between(0.95, 1)
               ]

    values = ['0% - 10%', '10% - 20%', '20% - 30%','30% - 40%',
              '40% - 50%','50% - 60%','60% - 70%','70% - 80%','80% - 90%','90% - 95%','95% - 100%']

    values_index = [1, 2,3,4,5,6,7,8,9,10,11]
    
    ###################################################################
    
    criteria2 = [X_eval['PREDICT_PROBA'].between(0.0, 0.5),
                X_eval['PREDICT_PROBA'].between(0.5, 1),             
               ]

    values2 = ['0% - 50%', '50% - 100%']

    values_index2 = [1, 2]
    
    #####################################################
 
    X_eval['PREDICT_CATEGORY'] = np.select(criteria, values, 0)
    X_eval['PREDICT_CATEGORY_INDEX'] = np.select(criteria, values_index, 0)

    X_eval['PREDICT_CATEGORY2'] = np.select(criteria2, values2, 0)
    X_eval['PREDICT_CATEGORY_INDEX2'] = np.select(criteria2, values_index2, 0)

    X_eval['TOTAL'] = 1 
    
    if y is not None:
    
        X_eval['ACIERTO(VP)'] = np.where( (X_eval['REAL']==1) & (X_eval['PREDICT']==1), 1 ,0)
        X_eval['FP'] = np.where( (X_eval['REAL']==0) & (X_eval['PREDICT']==1), 1 ,0)    

        X_eval_gb = X_eval.groupby(['PREDICT_CATEGORY_INDEX','PREDICT_CATEGORY']).agg({'TOTAL':'count','REAL':'sum'}).reset_index()
        X_eval_gb.sort_values(by='PREDICT_CATEGORY_INDEX', ascending=False,inplace=True)
        X_eval_gb.rename(columns={'REAL': 'DESERTORES','PREDICT_CATEGORY':'RANGO'}, inplace=True)
        del X_eval_gb['PREDICT_CATEGORY_INDEX']
        X_eval_gb.reset_index(drop=True,inplace=True)

        X_eval_gb['TOTAL %']=round(X_eval_gb['TOTAL']/X_eval_gb['TOTAL'].sum(),3)
        X_eval_gb['COBERTURA %']=round(X_eval_gb['DESERTORES']/X_eval_gb['DESERTORES'].sum(),3)
        
        
        X_eval_gb['PRECISION RANGO %']=round(X_eval_gb['DESERTORES']/X_eval_gb['TOTAL'],3)

        #X_eval_gb.index.name = 'N'

        
        
        if not url_dir:
            url_dir="reporte_modelo/out/"
        else:

            url_dir = '{}/{}'.format("reporte_modelo/out",url_dir)
            if not os.path.exists(url_dir):
                os.makedirs(url_dir)

        X_eval_gb.to_excel(url_dir+"df_agg_t.xlsx", encoding="utf-8")

        
        
        
        # Set colormap equal to seaborns light green color palette
        cm = sns.light_palette("red", as_cmap=True)

        return X_eval, (X_eval_gb.style
          .background_gradient(cmap=cm, subset=['PRECISION RANGO %'])
          .format({'TOTAL %': "{:.1%}"})  
          .format({'PRECISION RANGO %': "{:.1%}"})
          .format({'COBERTURA %': "{:.1%}"})
        )
    
    else:
        X_eval_gb = X_eval.groupby(['PREDICT_CATEGORY_INDEX','PREDICT_CATEGORY']).agg({'TOTAL':'count'}).reset_index()
        X_eval_gb.sort_values(by='PREDICT_CATEGORY_INDEX', ascending=False,inplace=True)
        X_eval_gb.rename(columns={'PREDICT_CATEGORY':'RANGO'}, inplace=True)
        del X_eval_gb['PREDICT_CATEGORY_INDEX']
        
        X_eval_gb['TOTAL %']=round(X_eval_gb['TOTAL']/X_eval_gb['TOTAL'].sum(),3)
        
        X_eval_gb.reset_index(drop=True,inplace=True)
        
        
        cm = sns.light_palette("blue", as_cmap=True)
        return X_eval, (X_eval_gb.style
          .background_gradient(cmap=cm, subset=['TOTAL %'])
          .format({'TOTAL %': "{:.1%}"})      
        )
        
#df_nom,df_agg = get_summary_evaluation(X_test,estimator_random,y_test)
#df_agg

#desertores predichos / desertores reales






def save_join_data(df,df_eval,url_dir=""):
    
    if not url_dir:
        url_dir="reporte_modelo/out/"
    else:
        url_dir = '{}/{}'.format("reporte_modelo/out",url_dir)
        if not os.path.exists(url_dir):
            os.makedirs(url_dir)
        print("reporte generado en : "+url_dir)
    
    specific_url = url_dir+"data.csv"
    specific_url_eval = url_dir+"data_eval.csv"
    
    df.to_csv(specific_url,index =False , encoding="utf-8") 
    df_eval.to_csv(specific_url_eval,index =False , encoding="utf-8") 
    
    



    

def exportar_para_dashborad(df_nom,df_nominal_eval,df_servicios,ID_PERSONA_EVAL,url_dir=""):

    df_result =pd.DataFrame({'ID_PERSONA':ID_PERSONA_EVAL.values,'RISK_SCORE':df_nom.PREDICT_PROBA.values}) 
    df_result.shape
    
    mapa_des_nivel = {'A1':'Inicial - Cuna','A2':'Inicial - Jardín',
                      'A3':'Inicial - Cuna-jardín',
                      'A5':'Inicial - Programa no escolarizado',
                      'B0':'Primaria','F0':'Secundaria'}
    
    mapa_gestion =   {1:'PÚBLICA',2:'PÚBLICA',3:'PRIVADA'}
    
    
    df_result_nom = pd.merge(df_result , df_nominal_eval, left_on=['ID_PERSONA'], right_on=['ID_PERSONA'], how='inner')
    df_result_nom['DSC_NIVEL'] = df_result_nom.ID_NIVEL.map(mapa_des_nivel)



    df_result_nom_geo = pd.merge(df_result_nom , df_servicios, left_on=['COD_MOD','ANEXO'],
                                 right_on=['COD_MOD','ANEXO'], how='inner')
    
    df_result_nom_geo['GESTION_DES'] = df_result_nom_geo.GESTION.map(mapa_gestion)


    df_result_nom_geo.rename(columns={'EDAD_AL_2020': 'EDAD','N_DOC':'DNI','CODGEO':'COD_GEO',
                                      'CODIGO_ESTUDIANTE':'COD_ESTUDIANTE' }, inplace=True)
    
    cls_export = ["COD_MOD","ANEXO","COD_GEO","GESTION_DES","ID_NIVEL","DSC_NIVEL","ID_GRADO","DSC_GRADO",
                  "ID_PERSONA","COD_ESTUDIANTE",
                  "DNI","SEXO","EDAD","APELLIDO_PATERNO","APELLIDO_MATERNO","NOMBRES","RISK_SCORE"]
    
    #specific_url = "reporte_modelo/out/"+url_dir+"listado_eval.xlsx"
    
    
    if not url_dir:
        url_dir="reporte_modelo/out/"
    else:

        url_dir = '{}/{}'.format("reporte_modelo/out",url_dir)
        if not os.path.exists(url_dir):
            os.makedirs(url_dir)
        print("reporte generado en : "+url_dir)
    
    specific_url = url_dir+"listado_eval.csv"
    
    #df_result_nom_geo[cls_export].to_excel(specific_url,index=False) 
    df_result_nom_geo[cls_export].to_csv(specific_url,index =False , encoding="utf-8")
    

    

   
    
def get_url_homo_nom(ANIO,ID_GRADO):
    
    if ANIO>=2019:
        if ID_GRADO>=10:
            url_nom = "../PROYECTO_AVISE/00.CARGA/00.HOMOGENEO_NOMINAL_SIAGIE/NOMINAL_F0_{}.csv"
        if ID_GRADO>=4 and ID_GRADO<=9:
            url_nom = "../PROYECTO_AVISE/00.CARGA/00.HOMOGENEO_NOMINAL_SIAGIE/NOMINAL_B0_{}.csv"
    else:
        url_nom = "../PROYECTO_AVISE/00.CARGA/00.HOMOGENEO_NOMINAL_SIAGIE/NOMINAL_{}.csv"
    
    return url_nom.format(ANIO)


def load_homogeneo_nominal(ANIO,ID_GRADO):
    
    dtypes_columns = {'COD_MOD': str,
                  'ANEXO':int,
                  'UBIGEO_NACIMIENTO_RENIEC':str,
                  'N_DOC':str,
                  'CODIGO_ESTUDIANTE':str,
                  'NUMERO_DOCUMENTO':str,
                  'NUMERO_DOCUMENTO_APOD':str,
                  'CODOOII':str
                  }
    
    columns_n         = ['COD_MOD', 'ANEXO', 'ID_NIVEL','ID_GRADO','DSC_GRADO','ID_PERSONA','CODIGO_ESTUDIANTE','N_DOC',
                         'SEXO','EDAD_AL_2019','APELLIDO_PATERNO','APELLIDO_MATERNO','NOMBRES'
                         ]  
    
    
    iter_csv_n = pd.read_csv(get_url_homo_nom(ANIO,ID_GRADO),encoding="latin-1",sep="|",
                               dtype=dtypes_columns,iterator=True, chunksize=100000,usecols=columns_n)
    
    dataSet_n = pd.concat([chunk[chunk['ID_GRADO'] == ID_GRADO] for chunk in iter_csv_n])
    if ANIO==2020:
        dataSet_n.rename(columns={'EDAD_AL_2019': 'EDAD_AL_2020' }, inplace=True)
    return dataSet_n


def get_df_standarized(X_test,X_t_eval):
    columns_to_add = list(set(X_test.columns.tolist()) - set(X_t_eval.columns.tolist()))
    columns_to_delete = list(set(X_t_eval.columns.tolist()) - set(X_test.columns.tolist()))

    for column in columns_to_add:        
        X_t_eval[column]=0    

    for column in columns_to_delete:
        if column in X_t_eval.columns:
            del X_t_eval[column]

    return X_t_eval[X_test.columns.tolist()]  