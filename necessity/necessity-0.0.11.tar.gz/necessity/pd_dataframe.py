from __future__ import annotations

from collections import Counter
from itertools import chain
from typing import List

import pandas as pd


def count_column(dataframe: pd.DataFrame,
                  column_name: str,
                  normalize: bool = False) -> pd.Series:
    return dataframe[column_name].value_counts(normalize=normalize)


def sample_by_percentile(dataframe: pd.DataFrame,
                         column_name: str,
                         bins: List[float],
                         sample_sizes: List[int],
                         random_seed: int = 42,
                         auto_adjust: bool = True) -> List:
    """ From https://stackoverflow.com/q/65222324/610569 """
    # Check that sample sizes are coherent with no. of bins.
    assert len(sample_sizes) == len(bins) -1
    # Count the colum
    df_percent = count_column(dataframe, column_name, normalize=True)
    labels = range(len(bins)-1)

    # Label each key with their bin labels.
    df_sample = pd.cut(df_percent[::-1].cumsum(),  # Accumulate percentage
                                  bins=bins,       # Percentile bins, e.g. [0.0, 0.25, 0.75, 1.0]
                                  labels=labels,   # Bin labels.
                                 ).fillna(float(labels[-1])).astype(int)  # Convert the bin numbers to int.

    # Compute new sample size according to the percentile bins.
    label_counts = Counter(df_sample)
    new_samplesizes = {l:min(s, label_counts[l]) for l, s in zip(labels, sample_sizes)}

    # TODO: We should have an experimental feature to automatically
    #       readjust sample size according the how the bins are distributed.
    if auto_adjust:
        pass

    return list(pd.concat(df_sample[df_sample==l].sample(
            new_samplesizes[l]) for l in new_samplesizes).index)


def sum_str(*strings):
    return list(chain(*strings))


def count_x_concat_y(dataframe, column_x, column_y, concat_func=sum):
    count_x = dataframe[column_x].value_counts()
    concat_y = dataframe.groupby(column_x).agg({column_y: concat_func})
    return concat_y.join(count_x).rename({column_x:'count'}, axis=1)


__all__ = ['count_column', 'sample_by_percentile', 'count_x_concat_y', 'sum_str']
