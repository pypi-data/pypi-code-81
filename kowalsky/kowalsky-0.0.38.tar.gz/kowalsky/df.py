import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import missingno as msno
from kowalsky.logs.utils import calc_percent
from sklearn.model_selection import train_test_split


def corr(ds, y_col):
    return abs(ds.corr()[y_col]).sort_values()


def handle_outliers(df_raw, columns, drop=True, upper_quantile=.95,
                    lower_quantile=.05, verbose=False):
    df = df_raw.copy()

    out_cols = []
    for ix, col_value in enumerate(columns):
        col_in_df = isinstance(col_value, str)

        if col_in_df:
            if col_value not in df: continue
            column = df[col_value]
        else:
            column = col_value

        upper_lim = column.quantile(upper_quantile)
        lower_lim = column.quantile(lower_quantile)

        if not drop:
            if col_in_df:
                df.loc[(column > upper_lim), col_value] = upper_lim
                df.loc[(column < lower_lim), col_value] = lower_lim
            else:
                out_col = column.copy()
                out_col[column > upper_lim] = upper_lim
                out_col[column < lower_lim] = lower_lim
                out_cols.append(out_col)
        else:
            ix = (column < upper_lim) & (column > lower_lim)
            df = df[ix]
            if not col_in_df:
                out_col = column.copy()
                out_cols.append(out_col[ix])

        if verbose: print(f"Completed: {column}, {calc_percent(ix + 1, len(columns))}")
    return df, out_cols


def transform(df_raw, columns, fn=np.log1p, verbose=False):
    df = df_raw.copy()
    for ix, column in enumerate(columns):
        if column in df:
            df[column] = df[column].transform(fn)

        if verbose: print(f"Completed: {column}, {calc_percent(ix + 1, len(columns))}")

    return df


def drop(df_raw, columns):
    df = df_raw.copy()
    for column in columns:
        if column in df:
            df.drop(column, axis=1, inplace=True)

    return df


def group_by_mean(df_raw, pairs):
    df = df_raw.copy()
    for group_col, agr_col in pairs:
        if group_col in df and agr_col in df:
            df = pd.merge(df, df.groupby(group_col)[agr_col].mean(),
                          left_on=group_col, right_on=group_col, suffixes=('', f'_{group_col}_mean'))

    return df


def group_by_max(df_raw, pairs):
    df = df_raw.copy()
    for group_col, agr_col in pairs:
        if group_col in df and agr_col in df:
            df = pd.merge(df, df.groupby(group_col)[agr_col].max(),
                          left_on=group_col, right_on=group_col, suffixes=('', f'_{group_col}_max'))
    return df


def group_by_min(df_raw, pairs):
    df = df_raw.copy()
    for group_col, agr_col in pairs:
        if group_col in df and agr_col in df:
            df = pd.merge(df, df.groupby(group_col)[agr_col].min(),
                          left_on=group_col, right_on=group_col, suffixes=('', f'_{group_col}_min'))
    return df


def scale(df_raw, columns, minMax=False):
    df = df_raw.copy()

    if minMax:
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()

    for col in columns:
        if col in df_raw:
            df[col] = scaler.fit_transform(np.array(df[col]).reshape(-1, 1)).reshape(-1)
    return df


def describe_missing_values(df):
    msno.bar(df)
    msno.matrix(df)
    msno.heatmap(df)


def read_dataset(ds, path, y_column, feature_selection_support, feature_selection_cols,
                 ignore=[], sample_size=None, stratify=True):
    if ds is None:
        ds = pd.read_csv(path)

    if sample_size is not None:
        ds, _ = train_test_split(ds, train_size=sample_size, stratify=ds[y_column] if stratify else None)

    X, y = ds.drop([y_column] + ignore, axis=1), ds[y_column]

    if feature_selection_support is None and feature_selection_cols is None:
        feature_selection_cols = X.columns

    return X[X.columns[feature_selection_support] if feature_selection_support is not None else feature_selection_cols], y


