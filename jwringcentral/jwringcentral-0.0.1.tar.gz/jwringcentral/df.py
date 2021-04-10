import pandas as pd
import numpy as np

def CommonColumns(df1, df2):
    return list(set(df1.columns).intersection(df2.columns))

def Percentiles(df, num):
    result = []
    for col in df.columns:
        if (df[col].dtype != 'float') and (df[col].dtype != 'int'):
            continue
        else:
            result.append(np.percentile(df[col], num))
    return result