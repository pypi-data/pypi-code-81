"""Gen row alignment from tset, bigger ymax first. Varous util functions for plotting."""
from typing import List, Tuple  # , Union

import numpy as np

# from logzero import logger


# fmt: off
def gen_row_align(
        tset: List[Tuple[int, int, float]],
        src_len: int,
        tgt_len: int,
) -> List[Tuple[int, int, float]]:
    # fmt: on
    """Gen proper rows for given triple_set.

    Arguments:
        [t_set {np.array or list}] -- [nll matrix]
        [src_len {int}] -- numb of source texts (para/sents)
        [tgt_len {int}] -- numb of target texts (para/sents)

    Returns:
        [np.array] -- [proper rows]

    buff = [
        (-1, -1, ""),
        (tgt_len, src_len, ""),
    ]

    for idx, loc in enumerate(buff):
        if loc[0] > elm0:
            break
    else:
        idx += 1  # last
    if elm[1] > buff[idx-1][1] and elm[1] < buff[idx][1]:
        buff.insert(idx, elm)

    """
    # t_set = np.array(tset, dtype="object")
    t_set = tset

    buff = [
        (-1, -1, 1.),
        (tgt_len, src_len, 1.),
    ]
    y0, yargmax, ymax = zip(*t_set)
    ymax = list(ymax)
    low_ = np.min(ymax) - 1

    for _ in t_set:
        argmax_ = int(np.argmax(ymax))
        elm = t_set[argmax_]
        ymax[argmax_] = low_

        elm0, elm1, elm2 = elm
        # position elm in buff
        for idx, loc in enumerate(buff):
            if loc[0] > elm0:
                break
        else:
            idx += 1  # last

        # insert elm in for valid elm
        # (within range inside two neighboring points)
        if elm[1] > buff[idx - 1][1] and elm[1] < buff[idx][1]:
            buff.insert(idx, elm)

        # In [378]: zh, en, sim = buff0[0]
        # In [379]: lines_en[en], lines_zh[zh], sim

    buff.pop()  # remove last
    buff.pop(0)  # remove first

    return buff
