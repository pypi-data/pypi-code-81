# Data handling and processing
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import ADASYN
from imblearn.under_sampling import NearMiss
from imblearn.over_sampling import SMOTENC
from imblearn.pipeline import make_pipeline as imbalanced_make_pipeline
import random
#import statsmodels.api as sm
import matplotlib.patches as mpatches
import time
#import mpld3
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA, TruncatedSVD

from sklearn.preprocessing import StandardScaler, RobustScaler

from sklearn.model_selection import train_test_split, RandomizedSearchCV, learning_curve,cross_validate
from unidecode import unidecode
# Data visualisation & images
import matplotlib.pyplot as plt
import seaborn as sns
import sys
# Pipeline and machine learning algorithms
from sklearn.preprocessing import LabelEncoder,label_binarize
from sklearn import preprocessing, decomposition, svm #, cross_validation
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_selection import SelectFromModel

from sklearn.metrics import *
#roc_auc_score ,f1_score,  accuracy_score,r2_score,mean_squared_error,neg_mean_absolute_error,
#neg_mean_squared_log_error,neg_median_absolute_error
    
from sklearn.externals import joblib
import random

import matplotlib.pylab as pl
import pandas as pd
import csv
import pyodbc

#from imblearn.over_sampling import SMOTE

import json

# Model fine-tuning and evaluation
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_predict

from xgboost import plot_importance
from xgboost import XGBClassifier

import lightgbm as lgb
import catboost as cb

import pickle
import os

import timeit    
import shap

from boruta import BorutaPy


from sklearn.metrics import roc_curve, precision_recall_curve, auc, make_scorer, recall_score, accuracy_score, precision_score, confusion_matrix, roc_auc_score

from scipy import optimize as op_sc




shap.initjs()

# def feature_sel_shap( X_train, y_train, X_val , y_val, min_shap = 0 , objective='binary' , metric_lgb='f1',num_class=2):
#     # print("---------aaa--------")
#     # X_train.loc[(X_train['NIVEL_INSTRUCCION_APOD_2017']=='NAN' ) , 'NIVEL_INSTRUCCION_APOD_2017'] = np.nan
#     # X_val.loc[(X_val['NIVEL_INSTRUCCION_APOD_2017']=='NAN' ) , 'NIVEL_INSTRUCCION_APOD_2017'] = np.nan

#     # X_train.loc[(X_train['UBIGEO_NACIMIENTO_RENIEC_2017']=='000000' ) , 'UBIGEO_NACIMIENTO_RENIEC_2017'] = np.nan
#     # X_val.loc[(X_val['UBIGEO_NACIMIENTO_RENIEC_2017']=='000000' ) , 'UBIGEO_NACIMIENTO_RENIEC_2017'] = np.nan

#     print("inicio del proceso: feature_sel_shap con  min_shap:"+str(min_shap))
#     train_cols = X_train.columns.tolist()

#     _cols = X_train.columns
#     _num_cols = X_train._get_numeric_data().columns
#     _categorical_columns_name = list(set(_cols) - set(_num_cols))


#     train_data = lgb.Dataset(X_train, label=y_train.astype(int), 
#                             feature_name=train_cols)
#     test_data = lgb.Dataset(X_val, label=y_val.astype(int), 
#                             feature_name=train_cols, reference=train_data)

#     # LGB parameters:
#     params = {'learning_rate': 0.05,
#             'boosting': 'gbdt', 
#             'objective': objective,
#             'num_leaves': 2000,
#             'min_data_in_leaf': 200,
#             'max_bin': 200,
#             'max_depth': 16,
#             'seed': 2018,
#             'nthread': 10,}

#     if(objective=='multiclass'):
#         params['num_class'] = num_class
#         params['metric'] = metric_lgb
    
#     print("entrenando para optener las variables mas importantes")
#     # LGB training:
#     lgb_model = lgb.train(params, train_data, 
#                         categorical_feature=_categorical_columns_name,
#                         num_boost_round=1000, 
#                         valid_sets=(test_data,), 
#                         valid_names=('valid',), 
#                         verbose_eval=False, 
#                         early_stopping_rounds=20)


#     # DF, based on which importance is checked
#     X_importance = X_val
#     print("recuperando las variablwa impoetantes del modelo")
#     # Explain model predictions using shap library:
#     explainer = shap.TreeExplainer(lgb_model)
#     print("TreeExplainer...done")
#     shap_values = explainer.shap_values(X_importance)
#     print("shap_values...done")

#     shap_sum = np.abs(shap_values).mean(axis=0)
#     print("shap_sum...done")
#     importance_df = pd.DataFrame([X_importance.columns.tolist(), shap_sum.tolist()]).T
#     importance_df.columns = ['column_name', 'shap_importance']
#     importance_df = importance_df.sort_values('shap_importance', ascending=False)
   

#     return shap_values,X_importance,importance_df



def hf_build_model(split_config=None,model_config=None):  

    min_shap = model_config.get('min_shap')  
    #score = model_config.get('score')   #scoring = {'roc_auc': 'f1','recall': 'precision'}
    
    metric_lgb = model_config.get('metric_lgb') 
    score_rs = model_config.get('score_rs') 
    
    objective = model_config.get('objective')
    best_params = model_config.get('best_params')
    num_class = model_config.get('num_class')
    
    if(objective is None):
        objective = 'binary'
    
    n_splits = 10
    kfold = StratifiedKFold(n_splits=n_splits, shuffle=True)

    #model_validaded = model = X_train= X_val = X_test = y_train = y_val = y_test = X_train_full =y_train_full = None
    X_train, X_val , X_test , y_train , y_val , y_test = hf_train_test_split(**split_config)

#     shap_values,X_importance, importance_df = feature_sel_shap(X_train, y_train, X_val , y_val 
#                                                       , min_shap,objective=objective , metric_lgb=metric_lgb,num_class=num_class )

#    return shap_values, X_importance, importance_df
    if(model_config.get('importance') is None or model_config.get('importance')=='shap'):
        print("0) Obteniendo variables importantes")
        zero_features, feature_importances = feature_sel_shap(X_train, y_train, X_val , y_val 
                                                              , min_shap,objective=objective , metric_lgb=metric_lgb,num_class=num_class )
        print("fin del proceso : 0")
    elif(model_config.get('importance')=='boruta'):
        zero_features, feature_importances = feature_sel_boruta(X_train, y_train)
    #zero_features, feature_importances = self.identify_zero_importance_features(X_train, y_train, score ,iterations=n_splits)

    X_train_full =  pd.concat(objs=[X_train, X_val ], axis=0).reset_index(drop=True)
    y_train_full =  np.concatenate([y_train,y_val])
    X_train = X_train.drop(columns = zero_features)
    X_val = X_val.drop(columns = zero_features)   
    X_test = X_test.drop(columns = zero_features) 
    X_train_full = X_train_full.drop(columns = zero_features)  

    start_time = timeit.default_timer()
    
    if(best_params is not None):
        print("Omitiendo calculo de hypermarametros")
        bp = best_params
    else:
        print("1) CALCULANDO LOS MEJORES HYPERPARAMETROS  ------")
        bm, bp = get_hyperparametros(X_train,y_train,X_val,y_val,
                                     score_rs=score_rs,metric_lgb=metric_lgb,_kfold=kfold,objective=objective,num_class=num_class)
    print(bp)
    #     #best_param = {'scale_pos_weight': 3, 'objective': 'binary', 'n_estimators': 450, 'max_depth': -1, 'learning_rate': 0.015}
    print("2) ENTRENANDO EL MODELO  ------")
    model_validaded = buildModel_LGBMClassifier(X_train,y_train,X_val,y_val, bp,metric_lgb=metric_lgb)
    # model_validaded_smote = self.buildModel_LGBMClassifier(X_train,y_train,X_val,y_val, best_param, smote = True)
    # print("---- TESTEANDO EL MODELO 2 smote ------") 
    # self.run_clasification(X_test,y_test,model_validaded_smote)

    print("3) TESTEANDO EL MODELO  ------") 
    run_clasification(X_test,y_test,model_validaded,score_rs=score_rs,objective=objective)

    print("3) RETORNANDO EL CLASIFICADOR VALIDO  ------") 
    print("Columnas del modelo: ",X_test.columns)
    return model_validaded,zero_features


def buildModel_LGBMClassifier(X_train,y_train,X_val,y_val, best_param,smote=False, metric_lgb='f1'):


    lgb_model = lgb.LGBMClassifier(**best_param)

    fit_params={
        'eval_metric':metric_lgb,
        'eval_set':[(X_val, y_val)], 
        'eval_names':['valid','train'],
        'early_stopping_rounds':10, 
        'feature_name': 'auto', # that's actually the default
        'categorical_feature': 'auto', # that's actually the default
        'verbose':False
    }


    if(smote):
        _cols = X_train.columns
        _num_cols = X_train._get_numeric_data().columns
        _categorical_columns_name = list(set(_cols) - set(_num_cols))
        _categorical_columns_index = [X_train.columns.get_loc(c) for c in _categorical_columns_name if c in X_train]

        print("categorica ..............")
        print(_categorical_columns_name)

        print("_num_cols ..............")
        print(_num_cols)

        smote_nc = SMOTENC(categorical_features=_categorical_columns_index, random_state=0)
        X_train_smote, y_train_smote = smote_nc.fit_resample(X_train,y_train)
        X_imputed_df = pd.DataFrame(X_train_smote, columns = X_train.columns)
        print("--------- imputed categorical ------")
        for c in _categorical_columns_name:                
            X_imputed_df[c] = X_imputed_df[c].astype('category') 

        for c in _num_cols:                
            X_imputed_df[c] = X_imputed_df[c].astype('float') 


        lgb_model.fit(X_imputed_df,y_train_smote,**fit_params)
    else:

        #lgb_model.fit(X_train, y_train,**fit_params)
        lgb_model.fit(X_train, y_train)



    return lgb_model



def get_hyperparametros(_X_train,_y_train,X_val,y_val, score_rs ='f1', metric_lgb='f1',_kfold=None , doSMOTE=False, gs=True,objective='binary',num_class=2):

    print("Optimizando del score_rs :",score_rs)

    gb_param_grid = {'learning_rate':[0.015,0.012,0.025,0.01,0.005],
                    #'num_leaves':[25,28,31,38,45,50,60,70,80],
                    #'metric': metric_lgb,
                    'max_depth': [-1],
                    'objective' : [objective],
                    'n_estimators':[150,160,180,170,200,250,300,350,400,450,500,550,600,650,700,750,800],#,
                    'scale_pos_weight':[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] , 


                    # 'colsample_bytree' : [0.65, 0.66,0.7,0.8,0.85,0.9,1.],
                    # 'subsample' : [0.5,0.6,0.7,0.75,0.80,0.85,1.],
                    # 'reg_alpha' : [0,0.25,0.5,0.8,1,1.2],
                    # 'reg_lambda' : [0,0.25,0.5,0.8,1,1.2,1.4]   

                    # 'min_child_samples': sp_randint(100, 500), 
                    # 'min_child_weight': [1e-5, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4],
                    # 'subsample': sp_uniform(loc=0.2, scale=0.8), 
                    # 'colsample_bytree': sp_uniform(loc=0.4, scale=0.6),
                    # 'reg_alpha': [0, 1e-1, 1, 2, 5, 7, 10, 50, 100],
                    # 'reg_lambda': [0, 1e-1, 1, 5, 10, 20, 50, 100]

                    }

#    if(objective=='multiclass'):
#         gb_param_grid['num_class'] = num_class
#         gb_param_grid['metric'] = metric_lgb
    # fit_params={
    #     'feature_name': 'auto', # that's actually the default
    #     'categorical_feature': 'auto' # that's actually the default
    # }

    fit_params={
                        "early_stopping_rounds":10, 
                        "eval_metric" : metric_lgb, 
                        "eval_set" : [(X_val,y_val)],
                        'eval_names': ['valid','train'],
                        'verbose': False,
                        'feature_name': 'auto', # that's actually the default
                        'categorical_feature': 'auto' # that's actually the default
                    }

    print("params to iterate : ",)
    model = lgb.LGBMClassifier()
    LGB_best =  LGB_best_param = LGB_SMOTE_best = gsLGB = gsLGB_SMOTE = None
    #

    if(gs): 
        print("...Optimizando hyperparametros y generando modelo 80 sm")
        #gsLGB = GridSearchCV(estimator = model ,param_grid = gb_param_grid,  scoring=score, n_jobs= 5,  cv=_kfold)  
        #score ['f1','precision']
        #score = {'F1': 'f1', 'PRECISION': 'precision'}
        gsLGB = RandomizedSearchCV(model, param_distributions=gb_param_grid, 
                                   scoring=score_rs ,  n_iter=40, cv=_kfold,n_jobs= 13, iid=False)
        #gsLGB.fit(_X_train,_y_train,**fit_params)
        
        if(objective=='multiclass'):
            __y_train = label_binarize(_y_train, classes=[0, 1, 2, 3])
            gsLGB.fit(_X_train,__y_train)
        else:
            gsLGB.fit(_X_train,_y_train)

        # _cols = _X_train.columns
        # _num_cols = _X_train._get_numeric_data().columns
        # _categorical_columns_name = list(set(_cols) - set(_num_cols))
        # _categorical_columns_index = [_X_train.columns.get_loc(c) for c in _categorical_columns_name if c in _X_train]

        # smote_nc = SMOTENC(categorical_features=_categorical_columns_index, random_state=0)
        # X_train_smote, y_train_smote = smote_nc.fit_resample(_X_train,_y_train)
        # X_imputed_df = pd.DataFrame(X_train_smote, columns = _X_train.columns)


        # for c in _categorical_columns_name:                
        #     X_imputed_df[c] = X_imputed_df[c].astype('category') 

        # for c in _num_cols:                
        #     X_imputed_df[c] = X_imputed_df[c].astype('float') 

        # gsLGB.fit(X_imputed_df,y_train_smote,**fit_params)


        LGB_best = gsLGB.best_estimator_ 
        print(LGB_best)
        print('Best params for {}'.format(score_rs))
        print(gsLGB.best_params_)
        LGB_best_param = gsLGB.best_params_
    else:
        print("...generando modelo")
        model.fit(_X_train,_y_train) 
        LGB_best = model

    if(doSMOTE):            
        #param = Nm/Nrm
        gsLGB_SMOTE = GridSearchCV(estimator = model ,param_grid = gb_param_grid,  scoring=score, n_jobs= 10,  cv=_kfold)
        smt = SMOTE()                 
        X_train_smote, y_train_smote = smt.fit_sample(_X_train , _y_train)
        gsLGB_SMOTE.fit(X_train_smote,y_train_smote)
        LGB_SMOTE_best = gsLGB_SMOTE.best_estimator_
        print('Best params for {}'.format(score_rs))
        print(gsLGB_SMOTE.best_params_)

        return LGB_best, LGB_SMOTE_best
    else:
        return LGB_best , LGB_best_param



    



def feature_sel_shap( X_train, y_train, X_val , y_val, min_shap = 0 , objective='binary' , metric_lgb='f1',num_class=2):
    # print("---------aaa--------")
    # X_train.loc[(X_train['NIVEL_INSTRUCCION_APOD_2017']=='NAN' ) , 'NIVEL_INSTRUCCION_APOD_2017'] = np.nan
    # X_val.loc[(X_val['NIVEL_INSTRUCCION_APOD_2017']=='NAN' ) , 'NIVEL_INSTRUCCION_APOD_2017'] = np.nan

    # X_train.loc[(X_train['UBIGEO_NACIMIENTO_RENIEC_2017']=='000000' ) , 'UBIGEO_NACIMIENTO_RENIEC_2017'] = np.nan
    # X_val.loc[(X_val['UBIGEO_NACIMIENTO_RENIEC_2017']=='000000' ) , 'UBIGEO_NACIMIENTO_RENIEC_2017'] = np.nan

    print("inicio del proceso: feature_sel_shap con  min_shap:"+str(min_shap))
    train_cols = X_train.columns.tolist()

    _cols = X_train.columns
    _num_cols = X_train._get_numeric_data().columns
    _categorical_columns_name = list(set(_cols) - set(_num_cols))


    train_data = lgb.Dataset(X_train, label=y_train.astype(int), 
                            feature_name=train_cols)
    test_data = lgb.Dataset(X_val, label=y_val.astype(int), 
                            feature_name=train_cols, reference=train_data)

    # LGB parameters:
    params = {'learning_rate': 0.05,
            'boosting': 'gbdt', 
            'objective': objective,
            'num_leaves': 2000,
            'min_data_in_leaf': 200,
            'max_bin': 200,
            'max_depth': 16,
            'seed': 2018,
            'nthread': 10,}

    if(objective=='multiclass'):
        params['num_class'] = num_class
        params['metric'] = metric_lgb
    
    print("entrenando para optener las variables mas importantes")
    # LGB training:
    lgb_model = lgb.train(params, train_data, 
                        categorical_feature=_categorical_columns_name,
                        num_boost_round=1000, 
                        valid_sets=(test_data,), 
                        valid_names=('valid',), 
                        verbose_eval=False, 
                        early_stopping_rounds=20)


    # DF, based on which importance is checked
    X_importance = X_val
    print("recuperando las variablwa impoetantes del modelo")
    # Explain model predictions using shap library:
    explainer = shap.TreeExplainer(lgb_model)
    print("TreeExplainer...done")
    shap_values = explainer.shap_values(X_importance)
    print("shap_values...done")
    
    if(objective=="multiclass"):
        shap_sum = np.abs(shap_values).mean(axis=0).mean(axis=0)
    else:  
        shap_sum = np.abs(shap_values).mean(axis=0).mean(axis=0)
    print("shap_sum...done")
    importance_df = pd.DataFrame([X_importance.columns.tolist(), shap_sum.tolist()]).T
    importance_df.columns = ['column_name', 'shap_importance']
    importance_df = importance_df.sort_values('shap_importance', ascending=False)
    

    
    zero_features = importance_df[importance_df['shap_importance']<=min_shap].column_name.values
    print("fin de : feature_sel_shap")
    return zero_features , importance_df



def hfm_predict_standalone(X_test,model,columns_to_ignore=[]):
    df_model = X_test.copy()

    #columns_to_ignore = ['ID_CLIENTE','ESTADO_DESEMBOLSO_COTIZA']
    #columns_to_ignore_plus = columns_to_ignore+zero_features.tolist()

    df_model.drop(columns_to_ignore,axis=1,inplace=True)


    le = preprocessing.LabelEncoder()
    for c in df_model.columns:
        col_type = df_model[c].dtype
        if col_type == 'object' or col_type.name == 'category':
            #print("column : "+str(c))
            df_model[c] = le.fit_transform(df_model[c])
            df_model[c] = df_model[c].astype('category') 


    #y_prob = model.predict_proba(df_model)[:, 1]
    y_pred = model.predict(df_model)
    return y_pred

def run_clasification(_X_test,_y_test,_model,_model_smote=None,doSMOTE=False,score_rs="f1",objective="binary"):


    colors = ['b','g','r','c','m','y','k','b']

    y_prob = _model.predict_proba(_X_test)[:, 1]
    #best_thr = op_sc.fmin(self.thr_to_accuracy, args=(_y_test, y_prob), x0=0.5)

    y_pred = _model.predict(_X_test)
    #y_pred = np.where(y_prob>=best_thr,1,0)


    if(doSMOTE):
        y_pred_smote = _model_smote.predict(_X_test)
        y_prob_smote = _model_smote.predict_proba(_X_test)[:, 1]

    mean_tpr = mean_smote_tpr = 0.0
    mean_fpr = mean_smote_fpr = np.linspace(0, 1, 100)


    print(classification_report(_y_test, y_pred))

    if(score_rs == 'roc_auc'):
        print('roc_auc_score: ',roc_auc_score(_y_test, y_pred))
    elif(score_rs == 'f1'):
         print('f1_score: ',f1_score(_y_test, y_pred))
    elif(score_rs == 'accuracy'):
         print('accuracy_score: ',accuracy_score(_y_test, y_pred))
    elif(score_rs == 'r2'):
         print('r2: ',r2_score(_y_test, y_pred))        
    elif(score_rs == 'neg_mean_squared_error'):
         print('mean_squared_error: ',mean_squared_error(_y_test, y_pred))   
    elif(score_rs == 'neg_mean_absolute_error'):
         print('neg_mean_absolute_error: ',neg_mean_absolute_error(_y_test, y_pred))      
    elif(score_rs == 'neg_mean_squared_log_error'):
         print('neg_mean_squared_log_error: ',neg_mean_squared_log_error(_y_test, y_pred))   
    elif(score_rs == 'neg_median_absolute_error'):
         print('neg_median_absolute_error: ',neg_median_absolute_error(_y_test, y_pred))  
    # print('recall_score: ',recall_score(_y_test, y_pred, average="binary"))
    # print('precision_score:',precision_score(_y_test, y_pred, average="binary"))
    # print('f1_score:',f1_score(_y_test, y_pred, average="binary"))

    if((score_rs=='roc_auc' or score_rs=='f1_score') and objective=="binary"):    
        # confusion matrix on the test data.
        print('\nMatriz de confucion para la data de prueba:')
        print(pd.DataFrame(confusion_matrix(_y_test, y_pred),
                        columns=['pred_neg', 'pred_pos'], index=['Negativo', 'Positivo']))


    test_indexes = _X_test.index.astype(int)
    probas = np.column_stack((test_indexes,y_prob*100,y_pred,_y_test))

    result = pd.DataFrame(data=probas[1:,1:],    # values
                            index=probas[1:,0],    # 1st column as index
                            columns=['RISK_SCORE','PREDICCION','REAL'])
    return result , _y_test , y_pred , y_prob




def hf_train_test_split( df=None,target_name=None,columns_to_drop=None, 
                        test_size=0.25,scaler=None,umbral_variables_similares=None,target_encoder=None):

    if(df is None or target_name is None):
        print("_df y target_name son parametros obligatorios")
    else:    
        df_model = df.copy()

        # Eliminando columnas no necesarias
        if(columns_to_drop is not None): 
            df_model.drop(columns_to_drop,axis=1,inplace=True)

        # Escalar datos numericos. Esto solo es valido para regresiones. Para modelos de arbol de desciciones no tiene efecto
        if(scaler is not None):    
            if(scaler=='StandardScaler'):
                std_scaler = StandardScaler()
            elif(scaler=='RobustScaler'):
                std_scaler = StandardScaler()
                #rob_scaler = RobustScaler()
            for idx,tp in enumerate(df_model.dtypes):
                if tp != 'object' and tp.name != 'category': 
                    df_model[df_model.columns[idx]] = std_scaler.fit_transform(df_model[df_model.columns[idx]].values.reshape(-1,1))


        # Convierte las variables categoricas en one-hot-encoding
            # columns_to_drop = []
            # for idx,tp in enumerate(df_model.dtypes):
            #     if tp == 'object' or tp.name == 'category': 
            #         df_dummies = pd.get_dummies(df_model[df_model.columns[idx] ],prefix=df_model.columns[idx] )
            #         df_model = pd.concat([df_model,df_dummies],axis=1)
            #         columns_to_drop.append(df_model.columns[idx])
            # df_model.drop(columns_to_drop,axis=1,inplace=True)  


        # Codificando y categorizando todas las variables de tipo    
        le = preprocessing.LabelEncoder()
        for c in df_model.columns:
            col_type = df_model[c].dtype
            if col_type == 'object' or col_type.name == 'category':
                #print("column : "+str(c))
                df_model[c] = le.fit_transform(df_model[c])
                df_model[c] = df_model[c].astype('category') 


        # aislando la variable dependiente de las independientes
        X = df_model.drop([target_name],1)   #Feature Matrix
        y = df_model.loc[:,target_name]
        #y_= df_model[[target_name]]
        if(target_encoder is not None and target_encoder):
            labels = preprocessing.LabelEncoder().fit_transform(y)
        else:
            labels = np.array(y)
        X_df = df_model.drop(target_name,1)
        students = df_model.index


        # Removiendo variables independientes que sean muy parecidas entre si
        if(umbral_variables_similares is not None):
            # Threshold for removing correlated variables
            threshold = umbral_variables_similares
            # Absolute value correlation matrix
            corr_matrix = X_df.corr().abs()
            # Upper triangle of correlations
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
            # Select columns with correlations above threshold
            to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
            # Remove the columns
            X_df = X_df.drop(columns = to_drop)


        # separando la data en train, val y test
        X_train, X_test, y_train, y_test = train_test_split(X_df, labels, test_size=test_size, stratify=labels, random_state=1)

        X_train_, X_val, y_train_, y_val  = train_test_split(X_train, y_train, test_size=test_size, stratify=y_train, random_state=1)


        #X_train, X_test, y_train, y_test = train_test_split(X_df, labels,stratify=labels, test_size=0.25)
        #return train_test_split(X_df, labels,stratify=labels, test_size=_test_size)
        return X_train_, X_val , X_test , y_train_ , y_val , y_test


    
