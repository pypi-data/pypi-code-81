import matplotlib.pylab as plt
import json
import os
import math
from helper_functions import plot_learning_curve,plot_confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report,average_precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.under_sampling import RandomUnderSampler
from sklearn import preprocessing
import seaborn as sns
import pandas as pd
import pyodbc
import numpy as np
from sklearn.model_selection import RepeatedKFold
from sklearn.feature_selection import RFECV
import pickle
import pyodbc
import missingno as msno
from nltk.corpus import stopwords
import nltk
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
import time
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV, StratifiedKFold
import string
from nltk.stem.snowball import SnowballStemmer
import nltk 
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from scipy.stats import itemfreq
from sklearn.metrics import roc_curve, precision_recall_curve, auc, make_scorer, recall_score, accuracy_score,precision_score, confusion_matrix, roc_auc_score

import matplotlib.pyplot as plt
import scikitplot as skplt
from sklearn.feature_selection import RFECV, SelectFromModel
import eli5
from eli5.sklearn import PermutationImportance
from eli5.permutation_importance import get_score_importances

from sklearn.utils import check_array, check_random_state  # type: ignore
from sklearn.inspection import permutation_importance
# shap muestra muchos warnings fastidiosos, hay que ignorarlos
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import shap
#import shap
import pandas as pd
from sklearn.metrics import f1_score
from scipy.stats import spearmanr
from scipy.cluster import hierarchy
from collections import defaultdict


n_splits = 5
kfold = StratifiedKFold(n_splits=n_splits, shuffle=True,random_state=2)
BASE_DIR="reporte_modelo/out"

def get_list_spw(y_train,multiple):
    #t_pos = df_join[df_join.DESERCION==1].DESERCION.count()
    #t_neg = df_join[df_join.DESERCION==0].DESERCION.count()
    
    t_pos = y_train[y_train==1].count()
    t_neg = y_train[y_train==0].count()
    
    scale_pos_weightround= round(t_neg/t_pos)
    if(multiple):
        list_scale_pos_weightround = []
        #list_scale_pos_weightround.append(scale_pos_weightround-50)
        list_scale_pos_weightround.append(scale_pos_weightround-30)
        list_scale_pos_weightround.append(scale_pos_weightround-10)
        list_scale_pos_weightround.append(scale_pos_weightround-5)
        #list_scale_pos_weightround.append(scale_pos_weightround-1)
        list_scale_pos_weightround.append(scale_pos_weightround)
        #list_scale_pos_weightround.append(scale_pos_weightround+1)
        list_scale_pos_weightround.append(scale_pos_weightround+5)
        list_scale_pos_weightround.append(scale_pos_weightround+10)
        list_scale_pos_weightround.append(scale_pos_weightround+50)
        #list_scale_pos_weightround.append(scale_pos_weightround+70)
        list_scale_pos_weightround.append(scale_pos_weightround+100)
        list_scale_pos_weightround.append(scale_pos_weightround+150)
        #list_scale_pos_weightround.append(scale_pos_weightround+200)
        #list_scale_pos_weightround.append(scale_pos_weightround+250)
        #list_scale_pos_weightround.append(scale_pos_weightround+350)
        
    else:      
        list_scale_pos_weightround = [scale_pos_weightround]
        
        #list_scale_pos_weightround = [scale_pos_weightround-5,scale_pos_weightround,scale_pos_weightround+5]
        #list_scale_pos_weightround = [scale_pos_weightround-1]
     
    print("Posibles scale_pos_weight : ",list_scale_pos_weightround)
    return list_scale_pos_weightround

def f1_eval_metric(y_true, y_pred):

    eval_result = f1_score(y_true, y_pred.round())
    return ("f1", eval_result, True)

def precision_eval_metric(y_true, y_pred):

    eval_result = precision_score(y_true, y_pred.round())
    return ("precision", eval_result, True)

def recall_eval_metric(y_true, y_pred):

    eval_result = recall_score(y_true, y_pred.round())
    return ("recall", eval_result, True)

def average_precision_eval_metric(y_true, y_pred):

    eval_result = average_precision_score(y_true, y_pred)
    return ("average_precision", eval_result, True)

def roc_auc_eval_metric(y_true, y_pred):

    eval_result = roc_auc_score(y_true, y_pred)
    return ("roc_auc", eval_result, True)




def search(pipeline, parameters, X_train, y_train, X_test, y_test, optimizer='grid_search', n_iter=None,
           score_rs='accuracy',url_dir=""):
    print("++++++++++++++++++++++++ INICIO - ESTIMAR MODELO ++++++++++++++++++++++++")        
    if(score_rs=="f1"):
        fn_eval=custom_eval_metric
    elif(score_rs=="precision"):
        fn_eval=precision_eval_metric
    elif(score_rs=="recall"):
        fn_eval=recall_eval_metric
    elif(score_rs=="average_precision"):
        fn_eval=average_precision_eval_metric  
    elif(score_rs=="roc_auc"):
        fn_eval=roc_auc_eval_metric
    else:
        fn_eval=custom_eval_metric
        
    parameters['clf__scale_pos_weight'] = get_list_spw(y_train,False)
    fit_params={"clf__early_stopping_rounds":400, 
                "clf__eval_metric" : fn_eval, 
                "clf__eval_set" : [(X_test,y_test)],
                'clf__eval_names': ['test'],
                'clf__verbose': 200,
                'clf__feature_name': 'auto', # that's actually the default
                'clf__categorical_feature': 'auto' # that's actually the default
               }
    
    if(score_rs=="r2" or score_rs=="neg_mean_squared_error" ):
        cv_ = n_splits
    else:
        cv_ = kfold
    
    start = time.time() 
    
    if optimizer == 'grid_search':
        grid_obj = GridSearchCV(estimator=pipeline,
                                param_grid=parameters,
                                cv=cv_,
                                refit=True,
                                n_jobs = 7,
                                return_train_score=False,
                                scoring = score_rs
                                )
        
        grid_obj.fit(X_train, y_train,)
    
    elif optimizer == 'random_search':
        print('RandomizedSearchCV -> Multiples Hyperparametros')
        grid_obj = RandomizedSearchCV(estimator=pipeline,
                            param_distributions=parameters,
                            cv=cv_,
                            n_iter=n_iter,
                            refit=True,
                            return_train_score=False,
                            scoring = score_rs,
                            n_jobs = 8,
                            verbose=True,          
                            random_state=375)
       
        grid_obj.fit(X_train, y_train,**fit_params)
    
    else:
        print('enter search method')
        return

    estimator = grid_obj.best_estimator_
    results = pd.DataFrame(grid_obj.cv_results_)
    best_params = grid_obj.best_params_
    

    
    if (True):
        print("")
        print("CV ",score_rs," RandomizedSearchCV :")
        print_cv_clf(url_dir,estimator,best_params,X_train,y_train,cv_,grid_obj)    
        print("")
        print('GridSearchCV -> scale_pos_weight')
        grid_obj = GridSearchCV(estimator=estimator, 
                                        param_grid={'clf__scale_pos_weight':get_list_spw(y_train,True)},
                                        scoring=score_rs,
                                        cv=cv_,
                                        n_jobs = 8,
                                        refit=True,
                                        verbose=True,
                                        )

        grid_obj.fit(X_train, y_train,**fit_params)

        estimator = grid_obj.best_estimator_
        results = pd.DataFrame(grid_obj.cv_results_)
        best_params = grid_obj.best_params_

        print("")
        print("CV ",score_rs," GridSearchCV :")
        print_cv_clf(url_dir,estimator,best_params,X_train,y_train,cv_,grid_obj)    
        print("")
        
    print("")   
    print("Time elapsed: ", time.time() - start)
    print("")
    
    #estimator_full = lgb.LGBMClassifier(**grid_obj.best_params_, silent=-1, verbose=-1)
    #estimator_full.fit(X_train, y_train,)
    #print("Parameter combinations evaluated: ",results.shape[0])
    #estimator.named_steps['clf'] = estimator_full
    print("++++++++++++++++++++++++ FIN - ESTIMAR MODELO ++++++++++++++++++++++++")        
    return results, estimator


def print_cv_clf(url_dir,estimator,best_params_,X_train,y_train,cv_,grid_obj):
    
    do_cv = True
    if(do_cv):
        '''
        cvs_recall = cross_val_score(estimator, X_train, y_train, cv=cv_,scoring="recall")
        cvs_precision = cross_val_score(estimator, X_train, y_train, cv=cv_,scoring="precision")
        cvs_f1 = cross_val_score(estimator, X_train, y_train, cv=cv_,scoring="f1")  
        cvs_average_precision = cross_val_score(estimator, X_train, y_train, cv=cv_,scoring="average_precision")
        '''
        cvs_mean_score =  grid_obj.cv_results_['mean_test_score'][grid_obj.best_index_] 
        cvs_std_score =  grid_obj.cv_results_['std_test_score'][grid_obj.best_index_] 


    
    #print("RandomizedSearchCV.best_score_ {}: ".format(score_rs), grid_obj.best_score_)    
            
    if not url_dir:
        
        
        if(do_cv):
            
            print("cvs_mean_score: ", cvs_mean_score)
            print("cvs_std_score: ", cvs_std_score)
            '''
            print("cv_mean_recall: ", cvs_recall.mean())
            print("cv_std_recall: ", cvs_recall.std())
            print("cv_mean_precision: ", cvs_precision.mean())
            print("cv_std_precision: ", cvs_precision.std())
            print("cv_mean_f1: ", cvs_f1.mean())
            print("cv_std_f1: ", cvs_f1.std())
            '''
        print("")
        print("Hyperparametros seleccionados:")
        print(best_params_)
    else:
        
        if(do_cv):
            dic_values = dict()
            dic_values['cvs_mean_score'] = cvs_mean_score
            dic_values['cvs_std_score'] = cvs_std_score        
            '''
            dic_values['cv_mean_recall'] = cvs_recall.mean()
            dic_values['cv_std_recall'] = cvs_recall.std()
            dic_values['cv_mean_precision'] = cvs_precision.mean()
            dic_values['cv_std_precision'] = cvs_precision.std()
            dic_values['cv_mean_f1'] = cvs_f1.mean()
            dic_values['cv_std_f1'] = cvs_f1.std()   
            '''
            df_cv_score = pd.DataFrame(dic_values.items(), columns=['Score', 'Value'])
            df_cv_score.to_csv(url_dir+"cv_score.csv",index =False , encoding="utf-8")

        
        dic_hp = best_params_
        df_hp = pd.DataFrame(dic_hp.items(), columns=['Param', 'Value'])
        df_hp.to_csv(url_dir+"best_params_.csv",index =False , encoding="utf-8")
    
    
def hyperopt(param_space, X_train, y_train, X_test, y_test, num_eval):
    
    start = time.time()
    
    def objective_function(params):
        clf = lgb.LGBMClassifier(**params)
        score = cross_val_score(clf, X_train, y_train, cv=5).mean()
        return {'loss': -score, 'status': STATUS_OK}

    trials = Trials()
    best_param = fmin(objective_function, 
                      param_space, 
                      algo=tpe.suggest, 
                      max_evals=num_eval, 
                      trials=trials,
                      rstate= np.random.RandomState(1))
    loss = [x['result']['loss'] for x in trials.trials]
    
    best_param_values = [x for x in best_param.values()]
    
    if best_param_values[0] == 0:
        boosting_type = 'gbdt'
    else:
        boosting_type= 'dart'
    
    clf_best = lgb.LGBMClassifier(learning_rate=best_param_values[2],
                                  num_leaves=int(best_param_values[5]),
                                  max_depth=int(best_param_values[3]),
                                  n_estimators=int(best_param_values[4]),
                                  boosting_type=boosting_type,
                                  colsample_bytree=best_param_values[1],
                                  reg_lambda=best_param_values[6],
                                 )
                                  
    clf_best.fit(X_train, y_train)
    
    print("")
    print("##### Results")
    print("Score best parameters: ", min(loss)*-1)
    print("Best parameters: ", best_param)
    print("Test Score: ", clf_best.score(X_test, y_test))
    print("Time elapsed: ", time.time() - start)
    print("Parameter combinations evaluated: ", num_eval)
    
    return trials





def report_result(estimator_random, X_train,y_train,X_test,y_test,shap_kernel=False, umbral = None, score = "",url_dir=""):
    
    model = estimator_random.named_steps['clf'] 
    model_name = type(model).__name__
    
    plt.savefig(url_dir+'precision_recall_curve.png', bbox_inches='tight')
    
    # save the model to disk
    filename = url_dir+'model.sav'
    pickle.dump(model, open(filename, 'wb'))

    #1.	Usar Area Under the Curve como metrica de performance para saber que tan bien funciona el modelo. (ok)
    y_pred = estimator_random.predict(X_test)
    
    
    
    
    if(model_name=='LGBMRegressor'):  
        print('\nR cuadrado y_test -  y_pred ')
        print('-------------------------------------------')        
        plt.figure()
        plt.scatter(x=y_test,y=y_pred) 
        plt.plot(y_test,y_test,c="red")
        rho = pd.Series(y_test.values).corr(pd.Series(y_pred))
        plt.title(rho**2)    
        plt.show()
    if(model_name=='LGBMClassifier' or model_name=='LogisticRegression' or model_name=='SVC'):
        unique_labels = sorted(pd.Series(y_pred).unique())
        total_labels = len(unique_labels)    
        predicted_probas = estimator_random.predict_proba(X_test)
        
        if(umbral is not None):
            new_y_pred = []
            print("predicted_probas: ",predicted_probas[:,1])
            for prob in predicted_probas[:,1]:
                if(prob>=umbral):
                    new_y_pred.append(1)
                else:
                    new_y_pred.append(0)   
                    
            print("original y_pred",y_pred)
            y_pred = new_y_pred            
            print("nuevo y_pred",y_pred)
        if(total_labels>1):
            skplt.metrics.plot_roc(y_test, predicted_probas)
            
            
            #X_sample.values, y_sample.values.ravel()      
            if not url_dir:
                plt.show()
            else:
                plt.savefig(url_dir+'roc_curve.png', bbox_inches='tight')
                plt.close()
                
            average_precision = average_precision_score(y_test.values.ravel(), predicted_probas[:,1])    
            disp = plot_precision_recall_curve(model, X_test.values, y_test.values.ravel())
            disp.ax_.set_title('2-class Precision-Recall curve: '
                               'AP={0:0.2f}'.format(average_precision))           
            if not url_dir:
                plt.show()
            else:
                plt.savefig(url_dir+'precision_recall_curve.png', bbox_inches='tight')
                plt.close()                

        #2.	Reportar en la tabla el % de false positives respecto al total de negatives para saber que porcentaje de no
        #dropouts terminamos clasificandolos como dropout de manera incorrecta.
        #Estos son una cantidad muy grande asi que vale la pena tener cuidado. (ok)
        #print('\nMatriz de confucion para la data de prueba:')
        #print('-------------------------------------------')
#         print(pd.DataFrame(confusion_matrix(y_test, y_pred, labels=[0,1]),
#                         columns=['pred_neg', 'pred_pos'], index=['Negativo', 'Positivo']))
        
        if(total_labels==2):
            #confusion matrix
            cm =  confusion_matrix(y_test, y_pred, labels=[0,1])
            # Plotting confusion matrix (custom help function)
            plot_confusion_matrix(cm, ["Negativo", "Positivo"],url_dir)

        else:
            #confusion matrix
            cm =  confusion_matrix(y_test, y_pred, labels=unique_labels)
            # Plotting confusion matrix (custom help function)
            plot_confusion_matrix(cm, ["Clase : " + str(s)  for s in unique_labels])             

            
            
        
        if not url_dir:
            print('\nReporte de clasificación:')
            print('-------------------------------------------')        
            print(classification_report(y_test, y_pred))
        else:
            report = classification_report(y_test, y_pred, output_dict=True)
            df_rep = pd.DataFrame(report).transpose()
            df_rep.to_csv(url_dir+"classification_report.csv", encoding="utf-8")
        #3.	Evaluar la contribucion de cada variable en la estimacion del modelo. (ok)
    
 
    if(model_name == 'LGBMClassifier' or model_name == 'LGBMRegressor'  ):  

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)
        #shap.force_plot(explainer.expected_value, shap_values, X_train)
        if not url_dir:
            print("############################### IMPORTANCIA DE VARIABLES ###################################") 
            shap.summary_plot(shap_values, X_test)
        else:
            fig = shap.summary_plot(shap_values, X_test,show=False )
            plt.savefig(url_dir+'importancia_variables.png', bbox_inches='tight')
            plt.close(fig)
        #shap.summary_plot(shap_values[1], X_train) 
    else:
        if(shap_kernel):

            X_train_summary = shap.kmeans(X_train, 10)
            explainer = shap.KernelExplainer(estimator_random.predict_proba, X_train_summary, link="logit")
            shap_values = explainer.shap_values(X_test, nsamples=100)
            shap.summary_plot(shap_values, X_test)
            #shap.summary_plot(shap_values[0], X_test)






def print_permutation_importance_eli5(model,X,y):
    
    def score_f1_eli5(X, y):
        y_pred = model.predict(X)
        return f1_score(y, y_pred.round())

    base_score, score_decreases = get_score_importances(score_f1_eli5, np.array(X), y)
    feature_importances = np.mean(score_decreases, axis=0)

    feature_importance_dict = {}
    for i, feature_name in enumerate(X.columns):
        fi = feature_importances[i]
        if(fi>0):
            feature_importance_dict[feature_name]=fi
    print("print_permutation_importance_eli5")    
    print(dict(sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)))
    return feature_importance_dict.keys() 



def print_importancia_variables(clf,X_train,y_train,url_dir):
    start = time.time()
    columns = X_train.columns.astype('<U28')
    result = permutation_importance(clf, X_train, y_train, n_repeats=5,
                                    random_state=42)
    
    feature_importance_dict = {}
    feature_importances = result.importances_mean
    
    for i, feature_name in enumerate(columns):
        fi = feature_importances[i]
        if(fi>0):
            feature_importance_dict[feature_name]=fi    
    
    
    perm_sorted_idx = result.importances_mean.argsort()

    tree_importance_sorted_idx = np.argsort(clf.feature_importances_)
    tree_indices = np.arange(0, len(clf.feature_importances_)) + 0.5

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    ax1.barh(tree_indices,
             clf.feature_importances_[tree_importance_sorted_idx], height=0.7)
    ax1.set_yticklabels(columns[tree_importance_sorted_idx])
    ax1.set_yticks(tree_indices)
    ax1.set_ylim((0, len(clf.feature_importances_)))
    ax2.boxplot(result.importances[perm_sorted_idx].T, vert=False,
                labels=columns[perm_sorted_idx])
    fig.tight_layout()
    
    
    if not url_dir:
        plt.show()
    else:
        plt.savefig(url_dir+'importancia_variables.png', bbox_inches='tight')
        plt.close()  
    
    #plt.show()
    print("Time elapsed print_importancia_variables : ", time.time() - start)
    
    #return feature_importance_dict.keys() 

        
def print_permutation_importance(model,X_test,y_test):
    columns = X_test.columns
    perm = permutation_importance(model, X_test, y_test, n_repeats=20,random_state=42, n_jobs=5,scoring="f1")
    
   
    means = perm.importances_mean
    fullList = pd.concat((pd.DataFrame(columns, columns = ['Variable']), 
                          pd.DataFrame(means, 
                                       columns = ['mean'])), axis = 1).sort_values(by='mean', ascending = False)
    #print('RandomForestClassifier - Feature Importance:')
    #print('\n',fullList,'\n')
    
    
    sorted_idx = perm.importances_mean.argsort()

    plt.figure(figsize=(10, 10))
    #fig, ax = plt.subplots()
    plt.boxplot(perm.importances[sorted_idx].T,
               vert=False, labels=X_test.columns[sorted_idx])
    plt.title("Permutation Importances (test set)")
    plt.tight_layout()
    plt.show()
    
    feature_name = fullList[fullList['mean']>0].Variable.tolist()
    
    return feature_name


    
def print_importancia_LGB(model,X_train):

    columns = X_train.columns
    coefficients = model.feature_importances_.reshape(X_train.columns.shape[0], 1)
    absCoefficients = abs(coefficients)
    fullList = pd.concat((pd.DataFrame(columns, columns = ['Variable']), 
                          pd.DataFrame(absCoefficients, 
                                       columns = ['absCoefficient'])), axis = 1).sort_values(by='absCoefficient', ascending = False)
    print('LightGBM - Feature Importance:')
    print('\n',fullList,'\n')
    
    
    
    #coefficients = model.feature_importances_
    
    feature_imp = pd.DataFrame(sorted(zip(model.feature_importances_,X_train.columns)), columns=['Value','Feature'])
    plt.figure(figsize=(20, 10))
    sns.barplot(x="Value", y="Feature", data=feature_imp.sort_values(by="Value", ascending=False))
    plt.title('LightGBM Features (avg over folds)')
    plt.tight_layout()
    plt.show()

def print_Handling_Multicollinear_Feature(X_train):
    
    X_train = X_train.drop(X_train.std()[(X_train.std() == 0)].index, axis=1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 22))
    corr = spearmanr(X_train).correlation
    corr_linkage = hierarchy.ward(corr)
    dendro = hierarchy.dendrogram(
        corr_linkage, labels=X_train.columns.tolist(), ax=ax1, leaf_rotation=90,leaf_font_size=12,
    )
    dendro_idx = np.arange(0, len(dendro['ivl']))

    ax2.imshow(corr[dendro['leaves'], :][:, dendro['leaves']])
    ax2.set_xticks(dendro_idx)
    ax2.set_yticks(dendro_idx)
    ax2.set_xticklabels(dendro['ivl'], rotation='vertical')
    ax2.set_yticklabels(dendro['ivl'])
    fig.tight_layout()
    plt.show()

    
    cluster_ids = hierarchy.fcluster(corr_linkage, 1, criterion='distance')
    cluster_id_to_feature_ids = defaultdict(list)
    for idx, cluster_id in enumerate(cluster_ids):
        cluster_id_to_feature_ids[cluster_id].append(idx)
    selected_features = [v[0] for v in cluster_id_to_feature_ids.values()]
    
    X_train = X_train.iloc[:, selected_features]
    
    return X_train.columns.tolist()
    
    

def modelar(pipeline, parameters, X_train, y_train, X_test, y_test, optimizer='grid_search', n_iter=None,
            score_rs='accuracy',url_dir="",sel_var=False):

    log = True
    if not url_dir:
        url_dir=""
    else:
        log=False
        url_dir = '{}/{}'.format(BASE_DIR,url_dir)
        if not os.path.exists(url_dir):
            os.makedirs(url_dir)
        print("reporte generado en : "+url_dir)
    
    
    if log:
        print("###################### VALIDACIÓN 1: Cross-validation (Train Data) ##############################")  
        
        
    results_random, estimator_random , X_train , X_test = iterar_models(1,X_train,y_train,X_test,
                                                                        y_test, pipeline,parameters,optimizer,
                                                                        n_iter,score_rs,url_dir,sel_var)
        
        
    
    model = estimator_random.named_steps['clf'] 
    model_name = type(model).__name__  
    if(model_name == 'LGBMClassifier'):
        kfold = StratifiedKFold(n_splits=5, shuffle=True,random_state=2)
    else:
        kfold = 5
        
   
    
    #4. Evaluar la contribucion de la data (n de observaciones) sobre la estimacion del modelo.
    

    #comentado temporalmente por el apuro
    #plot_learning_curve(estimator_random,"Curva de aprendizaje",X_train,y_train,cv=kfold,score=score_rs,url_dir=url_dir)
    
    if log:
        print("############################### REPORTE DE RENDIMIENTO : Test Data ##########################################")
    report_result(estimator_random,X_train,y_train,X_test,y_test,score=score_rs,url_dir=url_dir)
    
    
    #LogisticRegression()  estimator_random
  
    return results_random, estimator_random , X_train , X_test



def iterar_models(n_iter_sel,X_train,y_train,X_test,y_test, pipeline,parameters,optimizer,n_iter,score_rs,url_dir,sel_var):
    start = time.time()
    #X_train.fillna(0,inplace=True)
    #X_test.fillna(0,inplace=True)

    if(sel_var):
        for i in range(n_iter_sel):

            results_random, estimator_random = search(pipeline, 
                                                      parameters,
                                                      X_train, y_train, 
                                                      X_test, y_test, optimizer, 
                                                      10,score_rs=score_rs,url_dir=url_dir)

            model = estimator_random.named_steps['clf'] 
            model_name = type(model).__name__  

            print_importancia_variables(model,X_train,y_train)        
            #selected_features = print_Handling_Multicollinear_Feature(X_train)
                         
            selected_features, max_score, rfecv = rfecv_opt(model ,9,X_train,y_train,score_rs,
                                                            StratifiedKFold(n_splits=5, shuffle=True,random_state=2),
                                                            url_dir)

            
            with open(url_dir+'columnas.txt', 'w') as outfile:
                json.dump(selected_features, outfile)

            X_train = X_train[selected_features]
            X_test = X_test[selected_features]
            print("X_train shape : ",X_train.shape)    
   
    print("before search")
    results_random, estimator_random = search(pipeline, 
                                              parameters,
                                              X_train, y_train, 
                                              X_test, y_test, optimizer, 
                                              n_iter,score_rs=score_rs,url_dir=url_dir)
    
    print("after search")
    model = estimator_random.named_steps['clf'] 
    model_name = type(model).__name__  
    print_importancia_variables(model,X_train,y_train,url_dir)   

    print("Time elapsed iterar_models : ", time.time() - start)
    return results_random, estimator_random , X_train , X_test




def rfecv_opt(model, n_jobs, X, y,score_rs, cv = None ,url_dir=""):
    print("++++++++++++++++++++++++ INICIO - SELECCION DE VARIABLES CON RFECV ++++++++++++++++++++++++")
    X_sample , y_sample = sample_small_data(X,y)
    start = time.time()
      

    rfecv = RFECV(estimator = model, step = 2, cv = cv,
                    n_jobs = n_jobs, scoring = score_rs, verbose = 0)
    
    #,min_features_to_select = 16
    rfecv.fit(X_sample.values, y_sample.values.ravel())
    print('Optimal number of features : %d', rfecv.n_features_)
    print('Max score with current model :', round(np.max(rfecv.grid_scores_), 3))
    # Plot number of features VS. cross-validation scores
    plt.figure()
    plt.xlabel('Number of features selected')
    plt.ylabel('Cross validation score ({})'.format(score_rs))
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    
        
    if not url_dir:
        plt.show()
    else:
        plt.savefig(url_dir+'rfecv_opt.png', bbox_inches='tight')
        plt.close()  

    important_columns = []
    n = 0
    for i in rfecv.support_:
        if i == True:
            important_columns.append(X.columns[n])
        n +=1
    
    print("Time elapsed rfecv_opt: ", time.time() - start)
    print("++++++++++++++++++++++++ FIN - SELECCION DE VARIABLES CON RFECV  ++++++++++++++++++++++++++")
    return important_columns, np.max(rfecv.grid_scores_), rfecv


def sample_small_data(X,y):
    t_poplacion = X.shape[0]
    t_muestra = 5000
    n_splits_ = round(t_poplacion/t_muestra)

    if(n_splits_>1):

        X_ = X.reset_index(drop=True)
        y_ = y.reset_index(drop=True)


        print(n_splits_)

        skf = StratifiedKFold(n_splits=n_splits_, shuffle=True, random_state=1)
        X_train_ = None
        Y_train_ = None
        for train_index, test_index in skf.split(X_, y_):

            
            X_train_ = X_.iloc[test_index]
            Y_train_ = y_[test_index]
            #print(X_train_.shape)
            break

        return X_train_, Y_train_
    else:

        return X, y

