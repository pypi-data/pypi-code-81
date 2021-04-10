import pandas as pd
import numpy as np
import sqlite3

def ImportLocal(path):
    '''
    Import a local stored file as a Pandas Data Frame
    Parameter:
        path: the file location
    Returns:
        dataframe(pandas.core.frame.DataFrame): a Pandas Data Frame
    '''
    global dataframe
    dataframe = pd.read_csv(path)
    return dataframe
    

def ImportSqlLite():
    '''
    Import a file from SqLite DB as a Pandas Data Frame
    Returns:
        auto(pandas.core.frame.DataFrame): a Pandas Data Frame with auto information
    '''
    con = sqlite3.connect("/Users/jiayiwang08/Desktop/sqlite/test.db")
    global auto
    auto = pd.read_sql_query('SELECT * FROM autodata', con)
    con.close()
    return auto


def ExportDB(df):
    '''
    Export a Pandas DF to SqLite DB
    Parameter:
        df(pandas.core.frame.DataFrame): a Pandas DF
    '''
    con = sqlite3.connect("/Users/jiayiwang08/Desktop/sqlite/test.db")
    df.to_sql('new_table', con, if_exists='replace', index=False)


def CommonColumns(df1, df2):
    '''
    Find the column names that two Pandas DF have in common
    Parameter:
        df1(pandas.core.frame.DataFrame): a Pandas DF
        df2(pandas.core.frame.DataFrame): a Pandas DF
    Return:
        result(list): the list of common column names shared by both DFs

    '''
    result = list(set(df1.columns).intersection(df2.columns))
    return result


def Percentiles(df, num):
    '''
    Return a specific percentile of all columns in a Pandas DF with numerical data type
    Parameter:
        df(pandas.core.frame.DataFrame): a Pandas DF
        num(int): a number between 0 and 100, specifies the percentile to return
    Return:
        result(list): the list containing the percentiles of all numerical columns in the DF

    '''
    result = []
    for col in df.columns:
        if (df[col].dtype != 'float') and (df[col].dtype != 'int'):
            continue
        else:
            result.append(np.percentile(df[col], num))
    return result