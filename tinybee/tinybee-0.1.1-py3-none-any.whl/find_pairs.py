"""Find pairs for a given cmat."""
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
import logzero
from logzero import logger
from tinybee.gen_iset import gen_iset
from tinybee.cmat2tset import cmat2tset


def find_pairs(
    cmat1: Union[List[List[float]], np.ndarray, pd.DataFrame],
    delta: float = 7,
    verbose: Union[bool, int] = False,
) -> List[Tuple[int, int, Union[float, str]]]:
    """Find pairs for a given cmat.

    Args:
        cmat: correlation/similarity matrix

    Returns:
        pairs + "" or metric (float)
    """
    if isinstance(verbose, bool):
        if verbose:
            verbose = 10
        else:
            verbose = 20
    logzero.loglevel(verbose)

    # if isinstance(cmat, list):
    cmat = np.array(cmat1)

    src_len, tgt_len = cmat.shape

    iset = gen_iset(cmat, verbose=verbose)
    tset = cmat2tset(cmat)

    *_, ymax = zip(*tset)
    ymax = list(ymax)
    low_ = np.min(ymax) - 1

    buff = [(-1, -1, ""), (tgt_len, src_len, "")]
    for _ in range(tgt_len):
        # postion max in ymax and insert in buff
        # if with range given by iset+-delta and
        # it's valid (do not exceed constraint
        # by neighboring points
        argmax = int(np.argmax(ymax))
        ymax[argmax] = low_
        elm = tset[argmax]
        elm0, *_ = elm

        # position elm in buff
        for idx, loc in enumerate(buff):
            if loc[0] > elm0:
                break
        else:
            idx += 1  # last

        # insert elm in for valid elm
        # (within range inside two neighboring points)
        if abs(tset[argmax][1] - iset[argmax][1]) <= delta:
            if elm[1] > buff[idx - 1][1] and elm[1] < buff[idx][1]:
                buff.insert(idx, elm)
        _ = """
        if abs(tset[loc][1] - iset[loc][1]) <= delta:
            if tset[loc][1] > buff[idx][1] and tset[loc][1] < buff[idx + 1][1]:
                buff.insert(idx + 1, tset[loc])
        # """

    # remove first and last entry in buff
    buff.pop(0)
    buff.pop()

    # return [(1, 1, "")]
    return buff
