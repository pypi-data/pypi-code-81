# -*- coding: utf-8 -*-

import core_helper.helper_general as hg
hg.set_base_path()

import lightgbm as lgb 
from scipy.stats import uniform as sp_uniform
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV

#import general as g
import src.Prj_Core.core_helper.model.general as g

def get_pipeline():
    '''
    lgb_pipe = pipeline.Pipeline([
        #
        #  metric="None", first_metric_only=True -> ignora binary_logloss en early_stopping_rounds
        ('clf', lgb.LGBMClassifier(metric="None", first_metric_only=True, importance_type="gain",n_jobs=4))
        ])        

    '''
    lgb_pipe = lgb.LGBMClassifier(metric="None", 
                                  first_metric_only=True, 
                                  importance_type="gain",
                                  use_missing=True,
                                  zero_as_missing=False,
                                  n_jobs=4)
    return lgb_pipe




def get_possible_params():
     
    lgb_param_random = {
        'metric':["None"],
        'first_metric_only':[True] ,
        'importance_type':["gain"], 
        'use_missing':[True],
        'zero_as_missing':[False],  
        'n_estimators':[10000] ,
        'objective':["binary"],  
        'random_state':[1] ,
        'num_leaves':list(range(7, 50)),
        'feature_fraction':sp_uniform(loc=0.2, scale=0.8),
        'bagging_fraction':sp_uniform(loc=0.2, scale=0.8),
        'bagging_freq':[1], 
        'n_jobs':[4],
        'reg_alpha': [0, 1e-1, 1, 2, 5, 7, 10, 50, 100],
        'reg_lambda': [0, 1e-1, 1, 5, 10, 20, 50, 100],
        'boosting_type': ['gbdt'],
        'learning_rate': [0.1,0.07,0.05,0.025,0.015,0.01,0.0085,0.007,0.005],
        'max_depth': [-1,1,3,5,10,15],       
       
    }

    return  lgb_param_random


def get_default_params():
    params = {}
    params['metric']="None" 
    params['first_metric_only']=True 
    params['importance_type']="gain"
    params['use_missing']=True 
    params['zero_as_missing']=False 
    params['n_estimators']=10000
    params['objective']="binary" 
    params['random_state']=1
    params['num_leaves']=15 
    params['feature_fraction']=0.7
    params['bagging_fraction']=0.7
    params['bagging_freq']=1
    params['n_jobs']=4
    return params


def lgb_model(X_train,y_train,X_test,y_test,score_rs='average_precision',params=None):

    fn_eval = g.get_fn_eval(score_rs)
    fit_params = get_fit_params(X_train,y_train,X_test,y_test,fn_eval)
  
                       
    model = lgb.LGBMClassifier(**params)
    print('---------- definicion del modelo ----------------')
    print(model)
    print('-------------------------------------------------')
    
    model.fit(X_train,y_train,**fit_params)
   
    return model


def lgb_model_rscv(X_train, y_train, X_test, y_test,score_rs='average_precision', params=None,n_iter=None,n_jobs = 4):
    
    print("++++++++++++++++++++++++ INICIO - ESTIMAR MODELO ++++++++++++++++++++++++")   
    fn_eval = g.get_fn_eval(score_rs)
    fit_params = g.get_fit_params(X_train,y_train,X_test,y_test,fn_eval)          

    cv_ = g.get_kfold()          
           
           
    print('RandomizedSearchCV -> Multiples Hyperparametros')
    grid_obj = RandomizedSearchCV(estimator=lgb.LGBMClassifier(),
                                  param_distributions=params,
                                  cv=cv_,
                                  n_iter=n_iter,
                                  refit=True,
                                  return_train_score=False,
                                  scoring = score_rs,
                                  n_jobs = n_jobs,
                                  verbose= True,          
                                  random_state=375)

    grid_obj.fit(X_train, y_train,**fit_params)

    estimator = grid_obj.best_estimator_
    results = pd.DataFrame(grid_obj.cv_results_)
    best_params = grid_obj.best_params_  
    
    print('------------mejores hyperparametros-------------')
    print(best_params)
    print('------------------------------------------------')
    
    return results, estimator , best_params

def get_fit_params(X_train,y_train,X_test, y_test,fn_eval):
 
    fit_params={"early_stopping_rounds":800, 
                "eval_metric" : fn_eval, 
                "eval_set" : [(X_train,y_train),(X_test,y_test)],
                'eval_names': ['train','test'],
                'verbose': 200,
                'feature_name': 'auto', # that's actually the default
                'categorical_feature': 'auto' # that's actually the default
               }    
    return fit_params