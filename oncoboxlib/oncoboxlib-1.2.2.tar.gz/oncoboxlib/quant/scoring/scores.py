from typing import Tuple

import numpy as np
import pandas as pd


def calc_pas(
        cnr: pd.DataFrame,
        arr: pd.DataFrame,
        gp: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    log_cnr = np.log(cnr)

    pas1 = (gp * arr).T.dot(log_cnr)

    temp = arr.abs().sum(axis=0)
    pas2 = pas1.div(temp, axis=0).fillna(0)

    return pas1, pas2


def calc_pal(
        cnr: pd.DataFrame,
        arr: pd.DataFrame,
        gp: pd.DataFrame
) -> pd.DataFrame:

    _, pas2 = calc_pas(cnr, arr, gp)
    return pas2 * 100
