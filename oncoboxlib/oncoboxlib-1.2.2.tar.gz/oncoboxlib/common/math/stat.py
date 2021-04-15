import pandas as pd


def quantile_normalization(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    ranks = df.rank(method='first').stack().astype(int)
    mean_rank = df.stack().groupby(ranks).mean()
    qn_df = df.rank(method='min').stack().astype(int).map(mean_rank).unstack()
    return qn_df
