import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')


def xg_time_map(match_id='dummy', figname='fig.png', display=True, save=True):
    df=scraper(match_id, save=False)
    plotter(df, save=save, display=display, filename=figname)
    
    
def scraper(match_id='match_id', save=False, filename='data.csv'):
    match_id=str(match_id)
    base_url = 'https://understat.com/match/'
    url = base_url+match_id
    
    #Use requests to get the webpage and BeautifulSoup to parse the page
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    scripts = soup.find_all('script')

    #get only the shotsData
    strings = scripts[1].string

    # strip unnecessary symbols and get only JSON data 
    ind_start = strings.index("('")+2 
    ind_end = strings.index("')") 
    json_data = strings[ind_start:ind_end] 
    json_data = json_data.encode('utf8').decode('unicode_escape')

    #convert string to json format
    data = json.loads(json_data)

    away=data['a']
    home=data['h']
    home.extend(away)

    df=pd.DataFrame(home)
    df.xG=df.xG.astype('float')
    df.X=df.X.astype('float')
    df.Y=df.Y.astype('float')
    df.minute=df.minute.astype('int')

    df.X=df.X*120
    df.Y=df.Y*80
    if(save==True):
        df.to_csv(filename, index=None)
    return(df)


def cumulative_calc(xG):
    temp=[]
    for i in range(len(xG)):
        temp.append(sum(xG[:i+1]))
    temp.append(max(temp))
    return temp

def plotter(df='df', display=True, save=True, filename='fig.png'):
    h_name=df.h_team.unique()[0]
    a_name=df.a_team.unique()[0]
    
    min_h=[0]
    xG_h=[0]
    min_a=[0]
    xG_a=[0]
    
    min_h.extend(list(df[df.h_a=='h'].minute))
    xG_h.extend(list(df[df.h_a=='h'].xG))
    min_a.extend(list(df[df.h_a=='a'].minute))
    xG_a.extend(list(df[df.h_a=='a'].xG))
    t_max=max(90, max(df.minute))
    min_h.append(t_max)
    min_a.append(t_max)
    
    goals=df[df.result=='Goal'].reset_index()
    own=df[df.result=='OwnGoal'].reset_index()
    
    cum_xG_a=cumulative_calc(xG_a)
    cum_xG_h=cumulative_calc(xG_h)
    
    fig,ax=plt.subplots(figsize=(10,6))
    fig.set_facecolor('#22312b')
    ax.patch.set_facecolor('#22312b')

    ax=plt.step(x=min_h, y=cum_xG_h, where='post', color='orange', label=h_name)
    ax=plt.step(x=min_a, y=cum_xG_a, where='post', color='red', label=a_name)
    for i in range(goals.shape[0]):
        if goals.h_a[i]=='a':
            time=goals.minute[i]
            idx=min_a.index(time)
            while min_a[idx]==min_a[idx+1]:
                idx=idx+1
            plt.scatter(x=time,y=cum_xG_a[idx], color='white')

        if goals.h_a[i]=='h':
            time=goals.minute[i]
            idx=min_h.index(time)
            while min_h[idx]==min_h[idx+1]:
                idx=idx+1
            plt.scatter(x=time,y=cum_xG_h[idx], color='white') 
    
    for i in range(own.shape[0]):
        if own.h_a[i]=='a':
            time=own.minute[i]
            time_opp=max([x for x in min_h if x<time])
            print(time)
            plt.scatter(x=time,y=cum_xG_h[min_h.index(time_opp)], color='red')
        if own.h_a[i]=='h':
            time=own.minute[i]
            time_opp=max([x for x in min_a if x<time])
            plt.scatter(x=time,y=cum_xG_a[min_h.index(time_opp)], color='red')            

    plt.xticks([15,30,45,60,75,90], color='white')
    plt.yticks(color='#FFFFFF')
    plt.tight_layout()
    plt.legend()
    if save ==True:
        plt.savefig(filename)
    if display==True:
        plt.show()