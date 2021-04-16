from typing import Union, List

import pandas as pd
import numpy as np


def load_data(
        filepath: str,
        target: str,
        exclude: Union[List[str], None] = None,
        drop_inf: bool = False,
        non_zero_cols: Union[List[str], None] = None,
        normalize: bool = False
) -> pd.DataFrame:
    data = pd.read_csv(filepath)
    if exclude is not None:
        data = data.drop(exclude, axis=1)

    data[target] = data[target].astype(int)
    if drop_inf:
        data = data.replace([np.inf, -np.inf], np.nan).dropna()

    if non_zero_cols is not None:
        data = data[~(data.loc[:, non_zero_cols] == 0).any(axis=1)]

    if normalize:
        data = (data - data.min()) / (data.max() - data.min())

    return data
