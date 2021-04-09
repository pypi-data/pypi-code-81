"""Genereat align set (aset) based on pset, src_lang and tgt_len."""
from typing import List, Tuple, Union
from itertools import zip_longest

# from logzero import logger


# fmt: off
def gen_aset(
        pset: List[Tuple[int, int, float]],
        src_len: int,
        tgt_len: int,
) -> List[Tuple[Union[str, float], Union[str, float], Union[str, float]]]:
    # fmt: on
    """Genereat align set (aset) based on pset, src_lang and tgt_len.

    src_len, tgt_len = cmat.shape
    zip_longest(..., fillvalue="")

    Args:
        pset: [x(lang2 zh), y(lang1 en), cos]
        src_len: lang1 (en)
        tgt_len: lang2 (zh)

    Returns:
        aset:
        [0...tgt_len, 0...src_len]
        [0, 0, .]
        ...
        [tgt_len-1, src_len-1, .]
    """
    buff = []
    pos0, pos1 = -1, -1
    for elm in pset:
        elm0, elm1, elm2 = elm
        interval = max(elm0 - pos0 - 1, elm1 - pos1 - 1)
        _ = zip_longest(range(pos0 + 1, elm0), range(pos1 + 1, elm1), [""] * interval, fillvalue="")
        buff.extend(_)
        buff.append(elm)
        pos0, pos1 = elm0, elm1

    # last batch if any
    elm0, elm1 = tgt_len, src_len
    interval = max(elm0 - pos0 - 1, elm1 - pos1 - 1)
    _ = zip_longest(range(pos0 + 1, elm0), range(pos1 + 1, elm1), [""] * interval, fillvalue="")
    buff.extend(_)

    return buff
