"""Plot tset."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from logzero import logger


# fmt: off
def plot_tset(
        res,
        xlabel="zh",
        ylabel="en",
        thirdcol="cos",
):
    # fmt: on
    """Plot triple set.

    cmat = ren600xzh400
    correlation mat: cmat.shape
            (600, 400)

    yargmax = cmat.argmax(axis=0)
    ymax = cmat.max(axis=0)

    res = [*zip(range(cmat.shape[0]), yargmax, ymax)]

    Args:
        triple set [int, int, flot]

    Returns:
        sns.scatter plot
        fig, ax
    """
    shape = np.array(res).shape
    if len(shape) != 2:
        logger.error("shape length not equal to 2: %s", shape)
        raise Exception("Expect 2-d data")

    fig, ax = plt.subplots()

    if shape[1] == 2:
        # df_res = pd.DataFrame(res, columns=["lang2", "argmax"])
        # sns.relplot(x="lang2", y="argmax", data=df_res, ax=ax)
        df_res = pd.DataFrame(res, columns=[xlabel, ylabel])
        sns.scatterplot(x=xlabel, y=ylabel, data=df_res, ax=ax)

        if 'get_ipython' not in globals():
            logger.info("\n\tKill the plot (ctrl-w or click the cross) to continue.")
            plt.show(block=True)

        # return fig, ax
        return None

    if shape[1] == 3:
        # df_res = pd.DataFrame(res, columns=["lang2", "argmax", thirdcol])

        # sns.relplot(x="lang2", y="argmax", size=thirdcol, hue=thirdcol, sizes=(1, 110), data=df_res)

        df_res = pd.DataFrame(res, columns=[xlabel, ylabel, thirdcol])
        sns.scatterplot(x=xlabel, y=ylabel, size=thirdcol, hue=thirdcol, sizes=(1, 110), data=df_res, ax=ax)

        if 'get_ipython' not in globals():
            logger.info("\n\tKill the plot (ctrl-w or click the cross) to continue.")
            plt.show(block=True)

        # return fig, ax
        return None
