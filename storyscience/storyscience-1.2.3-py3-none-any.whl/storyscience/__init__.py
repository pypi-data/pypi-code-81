from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode,iplot
import plotly.express as px

def Subbhashit():
    return ('Hi Vro')

def Shree():
    return ("HI SHREE")

def Shivang():
    return "HI GUJJU"


def Count(x):
    dictionary = dict()
    array = list(x)
    countArray = dict(Counter(array))
    return countArray


def Impute(array,method='mean'):
    arr = list(array)
    pos = []
    for i in range(len(arr)):
        if np.isnan(arr[i]):
            pos.append(i)
    for i in pos:
        arr.remove(arr[i])
    if method=='mean':
        for i in pos:
            key = int(sum(arr)/len(arr))
            arr.insert(i,key)
    elif method=='mode':
        for i in pos:
            dictionary = dict(Counter(arr).most_common(1))
            key = int(list(dictionary.keys())[0])
            arr.insert(i,key)
    return arr
    
def ZScore(data,threshold=1):
    threshold = 3
    outliers = []
    arr = list(data)
    mean = np.mean(arr)
    std = np.std(arr)
    for i in arr:
        z = (i-mean)/std
        if z > threshold:
            outliers.append(i)
    return outliers 

def SinglePlot(arr):
    fig, ax =plt.subplots(2,2)
    fig.set_size_inches(12.7, 10.27)
    
    plt.subplot(2,2,1)
    arr.value_counts().tail().plot(kind='pie',figsize=(15,10))
    
    sns.distplot(arr,ax=ax[0,1])
    
    plt.subplot(2, 2,3)
    arr.value_counts().tail().plot(kind='bar',color=['c','y','r'],figsize=(15,10))
    
    sns.boxplot(arr,ax=ax[1,1])
    
    fig.show()

def IQR(data,arg1=75,arg2=25):
    q3, q1 = np.percentile(data, [arg1 ,arg2])
    iqr = q3 - q1
    return iqr

def Describe(data):
    l = list(data.columns)
    length = []
    mini = []
    maxi =[]
    mean = []
    median = []
    mode = []
    typ =[]
    std =[]
    std=[]
    types = ['float64','int64']
    for  i in l:
        typ.append(data[i].dtype)
        length.append(len(data[i]))
        mini.append(min(data[i]))
        maxi.append(max(data[i]))
        if data[i].dtype in types:
            mean.append(data[i].mean())
            median.append(data[i].median())
            mode.append(data[i].mode()[0])
            std.append(np.std(data[i]))
            
        else:
            mean.append(np.nan)
            median.append(np.nan)
            mode.append(np.nan)
            std.append(np.nan)
            
        
    df = pd.DataFrame([typ,length,mini,maxi,mean,median,mode,std], index=['Type','Length','Minimum','Maximum','Mean','Median','Mode','STD'] ,columns = l)
    return df

def Chloropleth(data , title='' , hue =''):
    countries=data.value_counts()
    f= go.Figure(data=go.Choropleth(
        locations=countries.index,
        z =countries, 
        locationmode = 'country names', 
        colorscale =px.colors.sequential.Plasma,
        colorbar_title = str(hue),
    ))

    f.update_layout(
        title_text = str(title),
    )
    iplot(f)