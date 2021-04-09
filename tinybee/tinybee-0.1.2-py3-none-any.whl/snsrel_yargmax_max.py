"""Plot argmax and max."""
#
import numpy as np
import pandas as pd

# import matplotlib.pyplot as plt
import seaborn as sns

from logzero import logger


def plot_argmax(yargmax, ymax=None):
    """Plot yargmx and ymax."""
    try:
        len_ = yargmax.shape[0]
    except Exception:
        len_ = len(yargmax)

    if ymax is not None:
        df = pd.DataFrame({"lang2": range(len_), "argmax": yargmax, "max": ymax})
        sns.relplot(x="lang2", y="argmax", size="max", hue="max", data=df)
    else:
        df = pd.DataFrame({"lang2": range(len_), "argmax": yargmax})
        sns.relplot(x="lang2", y="argmax", data=df)


def plot_tset(res):
    """Plot triple set.

    cmat = ren600xzh400
    correlation mat: cmat.shape
            (600, 400)

    yargmax = cmat.argmax(axis=0)
    ymax = cmat.max(axis=0)

    res = [*zip(range(cmat.shape[0]), yargmax, ymax)]
    """
    shape = np.array(res).shape
    if len(shape) != 2:
        logger.error("shape length not equal to 2: %s", shape)
        return

    if shape[1] == 2:
        df_res = pd.DataFrame(res, columns=["lang2", "argmax"])
        sns.relplot(x="lang2", y="argmax", data=df_res)
        return

    if shape[1] == 3:
        df_res = pd.DataFrame(res, columns=["lang2", "argmax", "max"])
        # fig = plt.figure(figsize=(8, 6))
        # ax = fig.add_subplot(111)
        # sns.lineplot(x="lang2", y="argmax", size="max", data=df_res, ax=ax)
        # sns.lineplot(x="lang2", y="argmax" data=df_res, ax=ax)

        # use this!!!
        # sns.scatterplot(x="lang2", y="argmax", data=df_res, size="max", hue="max", ax=ax)
        # sns.scatterplot(x="lang2", y="argmax", data=df_res, size="max", sizes=(10,100), hue="max", ax=ax)
        # sizes=(10,100)

        # ax.cla()
        # ax.invert_yaxis()

        sns.relplot(x="lang2", y="argmax", size="max", hue="max", data=df_res)
        return
