import numpy as np
import pandas as pd


def calc_exp_cv(x, min_num=3):
    nonna = x[pd.notna(x)]
    if len(nonna) < min_num:
        return np.nan
    values = nonna.astype(float).values
    cv = np.std(values, ddof=1) / np.mean(values)
    return cv


def count_missing_value(x):
    return len(x[np.isnan(x)])
