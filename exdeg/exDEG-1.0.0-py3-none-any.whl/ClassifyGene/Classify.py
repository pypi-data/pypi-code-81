import Pyomic
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import precision_recall_curve

def get_hit_rate(origin_data,neg,pos):
    '''
    Calculate the hit-rate of classifier

    Parameters
    ----------
    origin_data:dict
        A dictionary of samples and their true categories(0 or 1)
    neg:int
        The number of negative samples
    pos:int
        The number of positive samples

    Returns
    ----------
    value:list
        A list composed of tuples, each tuples incluede quota, its hit-rate
    avg:float
        average hit-rate
    '''

    total=neg+pos
    sorted_idx = reversed(sorted(origin_data))
    son,mum = 0,0
    avg = 0
    value = []
    for i in sorted_idx :
        # print ((i, origin_data[i]), end =" ")
        son += origin_data[i]
        mum += 1
        avg += son/mum * origin_data[i]
        value.append(son/mum)
    avg /= pos
    return value,avg


def get_Qrecall(origin_data,neg,pos):
    '''
    Calculate the Qrecall of classifier

    Parameters
    ----------
    origin_data:dict
        A dictionary of samples and their true categories(0 or 1)
    neg:int
        The number of negative samples
    pos:int
        The number of positive samples

    Returns
    ----------
    value:list
        A list composed of tuples, each tuples incluede quota, its Qrecall
    avg:float
        average Qrecall
    PEM:float
        Potential extract measure
    '''
    total=neg+pos
    sorted_idx = reversed(sorted(origin_data))
    son,mum = 0,pos
    value = []
    for i in sorted_idx :
        print ((i, origin_data[i]), end =" ")
        son += origin_data[i]
        value.append(son/mum)
    avg_Qrecall = sum(value[pos-1:])/(total-pos+1)
    
    PEM = (sum(value)-(total+1)/2)/(neg/2)
    return value,avg_Qrecall,PEM

def get_avg_hit_rate(origin_data,neg,pos):
    '''
    Calculate the average hit-rate of classifier

    Parameters
    ----------
    origin_data:dict
        A dictionary of samples and their true categories(0 or 1)
    neg:int
        The number of negative samples
    pos:int
        The number of positive samples

    Returns
    ----------
    avg:float
        average hit-rate
    '''
    total=neg+pos
    sorted_idx = reversed(sorted(origin_data))
    son,mum = 0,0
    avg = 0
    value = []
    for i in sorted_idx :
        # print ((i, origin_data[i]), end =" ")
        son += origin_data[i]
        mum += 1
        avg += son/mum * origin_data[i]
        value.append(son/mum)
    avg /= pos
    return avg

def get_avg_Qrecall(origin_data,neg,pos):
    '''
    Calculate the average Qrecall and PEM of classifier

    Parameters
    ----------
    origin_data:dict
        A dictionary of samples and their true categories(0 or 1)
    neg:int
        The number of negative samples
    pos:int
        The number of positive samples

    Returns
    ----------
    avg:float
        average Qrecall
    PEM:float
        Potential extract measure
    '''
    total=neg+pos
    sorted_idx = reversed(sorted(origin_data))
    son,mum = 0,pos
    value = []
    for i in sorted_idx :
        son += origin_data[i]
        value.append(son/mum)
    avg_Qrecall = sum(value[pos-1:])/(total-pos+1)
    
    PEM = (sum(value)-(total+1)/2)/(neg/2)
    return avg_Qrecall,PEM

def cal_classgene(raw_data,eg,cg,
                method='ROC',
                threshold=0.8):

    '''
    Calculate the performance of each gene as a classifier

    Parameters
    ----------
    raw_data:pandas.DataFrame
        DataFrame of data points with each entry in the form:[sample1','sample2'...],index=gene_name
    eg:list
        Columns name of the experimental group
        Sample:['lab1','lab2']
    cg:list
        Columns name of the control group
        Sample:['Ctrl1','Ctrl2']
    method:str
        Methods for evaluating classifier performance
        'ROC' or 'PEM'
    threshold:float
        The threshold to distinguish between positive and negative samples

    Returns
    ----------
    auc_pd/pem_pd:pandas.DataFrame
        DataFrame of data in the form:['gene','auc/pem','sig']
        sig:up/down/normal, it means the distinguish of classifier
    '''
    print("...Calculated the class value of each gene")
    auc_pd=pd.DataFrame(columns=['gene','auc','sig'])
    pem_pd=pd.DataFrame(columns=['gene','pem','sig'])
    for i in raw_data.index:
        gene_name=i
        #neg
        s1 = np.array(raw_data.loc[gene_name][cg])
        tt1=np.zeros(len(s1))
        neg=len(s1)
        #pos
        s2 = np.array(raw_data.loc[gene_name][eg])
        tt2=np.ones(len(s2))
        pos=len(s2)
        dic = dict(zip(np.append(s1,s2), np.append(tt1,tt2)))
        if(method=='ROC'):
            from sklearn.metrics import roc_curve, auc
            fpr, tpr, thresholds = metrics.roc_curve(np.append(tt1,tt2), np.append(s1,s2))
            roc_auc = auc(fpr, tpr)
            if(roc_auc>=threshold):
                auc_pd=auc_pd.append({'gene':gene_name,'auc':roc_auc,'sig':'up'},ignore_index=True)
            elif(roc_auc<=(1-threshold)):
                auc_pd=auc_pd.append({'gene':gene_name,'auc':roc_auc,'sig':'down'},ignore_index=True)
            else:
                auc_pd=auc_pd.append({'gene':gene_name,'auc':roc_auc,'sig':'normal'},ignore_index=True)
        if(method=='PEM'):
            avg,pem=get_avg_Qrecall(dic,neg,pos)
            if(pem>=threshold):
                pem_pd=pem_pd.append({'gene':gene_name,'pem':pem,'sig':'up'},ignore_index=True)
            elif(pem<=(0-threshold)):
                pem_pd=pem_pd.append({'gene':gene_name,'pem':pem,'sig':'down'},ignore_index=True)
            else:
                pem_pd=pem_pd.append({'gene':gene_name,'pem':pem,'sig':'normal'},ignore_index=True)
    if(method=='ROC'):
        return auc_pd
    elif(method=='PEM'):
        return pem_pd
    else:
        return None


def find_classifygene(raw_data,eg,cg,method='ROC',threshold=0.8):
    '''
    Calculate the performance of each gene as a classifier

    Parameters
    ----------
    raw_data:pandas.DataFrame
        DataFrame of data points with each entry in the form:[sample1','sample2'...],index=gene_name
    eg:list
        Columns name of the experimental group
        Sample:['lab1','lab2']
    cg:list
        Columns name of the control group
        Sample:['Ctrl1','Ctrl2']
    method:str
        Methods for evaluating classifier performance
        'ROC' or 'PEM'
    threshold:float
        The threshold to distinguish between positive and negative samples

    Returns
    ----------
    diffgene:pandas.DataFrame
        The gene expression matrix in the original expression matrix can distinguish positive and negative samples
    '''
    res_auc=cal_classgene(raw_data,eg,cg,method=method,threshold=threshold)
    if method=='ROC':
        res_auc_sort=res_auc.sort_values(by='auc',ascending=False)
    elif(method=='PEM'):
        res_auc_sort=res_auc.sort_values(by='pem',ascending=False)
    diffgene=res_auc_sort[res_auc_sort['sig']!='normal']
    return diffgene

def find_classifyDEG(raw_data,eg,cg,method='ROC',threshold=0.8,log2fc=-1):
    '''
    Calculate the performance of each gene as a classifier

    Parameters
    ----------
    raw_data:pandas.DataFrame
        DataFrame of data points with each entry in the form:[sample1','sample2'...],index=gene_name
    eg:list
        Columns name of the experimental group
        Sample:['lab1','lab2']
    cg:list
        Columns name of the control group
        Sample:['Ctrl1','Ctrl2']
    method:str
        Methods for evaluating classifier performance
        'ROC' or 'PEM'
    threshold:float
        The threshold to distinguish between positive and negative samples
    log2fc:float
        The threshold value of the difference multiple
        If it is -1, then use the column in the middle of the HIST diagram to filter

    Returns
    ----------
    result:pandas.DataFrame
        index is DEG's data index, columns=['pvalue','qvalue','FoldChange','log(pvalue)','log2FC','sig','size']
    '''
    res=find_classifygene(raw_data,eg,cg,method=method,threshold=threshold)
    print("...Calculated the differential expression gene by classification")
    result=Pyomic.find_DEG(raw_data.loc[res['gene']],eg=eg,cg=cg,log2fc=log2fc)
    return result

