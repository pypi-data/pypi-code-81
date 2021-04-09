"""Generate iset (interpolated set) from a given correlation matrix or list. iset can then be used as a guide for aligning texts."""
from typing import List, Tuple, Union

import numpy as np
import pandas as pd

# import joblib
# import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# from absl import app, flags
import logzero
from logzero import logger

from tinybee.lowess_pairs import lowess_pairs
from tinybee.gen_row_align import gen_row_align
from tinybee.interpolate_pset import interpolate_pset

# FLAGS = flags.FLAGS
# flags.DEFINE_boolean("debug", False, "print debug messages.", short_name="d")


# fmt: off
def gen_iset(
        cmat1: Union[List[List[float]], np.ndarray, pd.DataFrame],
        verbose: Union[bool, float] = False,
) -> List[Tuple[int, int]]:
    # fmt: on
    """Generate pset (pair set) from a given correlation matrix or list.

    Args:
        cmat: correlation (similarity) matrix
        verbose: show verbose messages
            show plotting (plot_flag set to True)
            when set to True or <= 10

    Returns:
        pair of integers as a guide for aligning
    """
    if isinstance(verbose, bool) is True:
        if verbose:
            verbose = 10
        else:
            verbose = 20
    logzero.loglevel(verbose)

    plot_flag = False
    if verbose <= 10:
        plot_flag = True

    # if isinstance(cmat, list):
    cmat = np.array(cmat1)

    logger.debug("cmat.shape: %s", cmat.shape)

    yhat = lowess_pairs(cmat)
    if plot_flag:
        df0 = pd.DataFrame(yhat, columns=["y00", "yargmax", "ymax"])
        fig, ax = plt.subplots()
        sns.scatterplot(data=df0, x="y00", y="yargmax", size="ymax", sizes=(1, 110))

        if "get_ipython" not in globals():
            plt.show(block=True)

    src_len, tgt_len = cmat.shape
    pset = gen_row_align(yhat, src_len, tgt_len)
    if plot_flag:
        df1 = pd.DataFrame(pset, columns=["y00", "yargmax", "ymax"])
        fig, ax = plt.subplots()
        sns.scatterplot(data=df1, x="y00", y="yargmax", size="ymax", sizes=(1, 110))

        if "get_ipython" not in globals():
            plt.show(block=True)

    iset = interpolate_pset(pset, tgt_len)
    if plot_flag:
        df2 = pd.DataFrame(iset, columns=["y00", "yargmax"])
        fig, ax = plt.subplots()
        sns.scatterplot(data=df2, x="y00", y="yargmax")

        if "get_ipython" not in globals():
            plt.show(block=True)

    # return [(1, 1)]
    return iset


_ = '''
def main(argv):
    """Test main."""
    logger.info(argv)
    if FLAGS.debug:
        logzero.loglevel(10)

    cmat = joblib.load("data/cmat.lzma")

    res = gen_iset(
        # [[1., 1.]],
        cmat,
        verbose=FLAGS.debug
    )
    # logger.debug("res: %s, %s", res, res[68])
    # logger.info("res: %s, %s", res, res[68])
    logger.debug("res[68]: %s", res[68])


if __name__ == "__main__":
    app.run(main)
    # python -m tinybee.gen_iset -d
# '''
