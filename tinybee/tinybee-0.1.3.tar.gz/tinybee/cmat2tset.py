"""Gen triple-set from a  matrix."""
from typing import List, Tuple, Union

import numpy as np
import pandas as pd


# fmt: off
def cmat2tset(
    cmat1: Union[List[List[float]], np.ndarray, pd.DataFrame],
    thirdcol: bool = True
) -> List[Union[Tuple[int, int], Tuple[int, int, float]]]:
    # fmt: on
    """Gen triple-set from a  matrix."""
    # if isinstance(cmat, list):
    cmat = np.array(cmat1)

    y00 = range(cmat.shape[1])  # cmat.shape[0] long time wasting bug
    yargmax = cmat.argmax(axis=0)

    if thirdcol:
        ymax = cmat.max(axis=0)

        res = [*zip(y00, yargmax, ymax)]  # type: ignore
        # to unzip
        # a, b, c = zip(*res)

        return res

    _ = [*zip(y00, yargmax)]  # type: ignore

    return _
