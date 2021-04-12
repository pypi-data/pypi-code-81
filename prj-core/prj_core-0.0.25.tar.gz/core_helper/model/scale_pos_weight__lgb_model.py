# -*- coding: utf-8 -*-
import core_helper.helper_general as hg
hg.set_base_path()

#import general as g
import src.Prj_Core.core_helper.model.general as g

#import lgb_model as l
import src.Prj_Core.core_helper.model.lgb_model as l


import math
from imblearn.under_sampling import RandomUnderSampler
import numpy as np
import pandas as pd
import core_helper.helper_plot as  hp
import time

def modelar(X_train,y_train,X_test,y_test,url):    
    start = time.time()

    N_p = y_train[y_train==1].count()
    N_n = y_train[y_train==0].count()

    alpha = (10000-N_p)/N_n
    params = l.get_default_params()
    params['pos_bagging_fraction'] = 1
    params['neg_bagging_fraction'] = 1
    params['scale_pos_weight'] = N_n/N_p

    ###################################################

    model = l.lgb_model(X_train,y_train,X_test,y_test,params=params)
    g.save_model(model,url)
    
    predicted_probas = model.predict_proba(X_test)   
    
    ##predicted_probas_t = model.predict_proba(X_t)
    ##y_prob_uno_t = predicted_probas_t[:,1]
        
    ##predicted_probas_t_mas_1 = model.predict_proba(X_t_mas_1)
    ##y_prob_uno_t_mas_1 = predicted_probas_t_mas_1[:,1]
    
     
    #kpis = hp.print_kpis_rendimiento_modelo(y_test,predicted_probas,url)   
    #hp.print_shap_plot(model,X_test,url)
    #print("Time elapsed: ", time.time() - start)
    #g.get_summary_evaluation2(X_test,predicted_probas,y_test,url)
  
    #return kpis , predicted_probas, y_prob_uno_t, y_prob_uno_t_mas_1
    return model , predicted_probas