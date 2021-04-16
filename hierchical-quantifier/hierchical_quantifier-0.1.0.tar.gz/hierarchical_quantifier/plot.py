"""
This module is used to plot the hierarchical quantifier using a scape plot.
"""

import matplotlib.pyplot as plt
import pitchscapes.plotting as pt
import numpy as np


def plot_scape(scape, ax=None, coord_kwargs=None, plot_kwargs=None):
    """
    Given a scape representation, this function plot the scape plot.

    :param scape: Scape representation of the hierarchical quantifier.
    :param ax: axis to plot of a figure.
    :param coord_kwargs: optional kwargs passed to `coords_from_times` function.
    :param plot_kwargs: optional kwargs passed to `scape_plot` function.

    """
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    corpus_len = scape.shape[0]

    res_norm = scape
    # remove the lower triangle
    index = np.arange(corpus_len)
    for i in index:
        for j in index:
            if j < i:
                res_norm[i, j] = -1

    pt.scape_plot_from_array(res_norm[res_norm > -1] / res_norm.max(), ax=ax, coord_kwargs=coord_kwargs,
                             plot_kwargs=plot_kwargs)
    plt.show()
