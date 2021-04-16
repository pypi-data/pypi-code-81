"""
quick.py
Written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from . import core

import izzy as iz
import numpy as np
import pandas as pd
from typelike import ArrayLike


# Create gradient
def gradient(cmap='ujet', n=256, figsize=(5, 2)):
    import matplotlib.pyplot as plt
    x = np.linspace(0, 1, n)
    if cmap == 'ujet':
        cmap = core.jet
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(np.vstack((x, x)), aspect='auto', cmap=cmap)
    plt.show()


# Create heatmap
def heatmap(data):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator
    from matplotlib.patches import Rectangle
    from scipy.spatial.distance import squareform
    import uplot as u
    u.set_mpl_theme()

    def heatmap(data, x_min=None, x_max=None, y_min=None, y_max=None, remove_diagonal=False):
        # Remove diagonal elements?
        for i in np.arange(data.shape[0]):
            for j in np.arange(data.shape[1]):
                if j < i + 2:
                    data[j, i] = np.nan

        # Define boundaries
        if x_min is None:
            x_min = 0
            x_max = data.shape[0]

        if y_min is None:
            y_min = 0
            y_max = data.shape[1]

        x_wid = (x_max - x_min) / (data.shape[0] - 1.)
        y_wid = (y_max - y_min) / (data.shape[1] - 1.)

        x_wid_h = x_wid / 2.
        y_wid_h = y_wid / 2.

        # Maximum of data set
        z_min = np.min(data[~np.isnan(data)])
        z_max = np.max(data[~np.isnan(data)])

        # Define initial figure
        fig = plt.figure()
        ax = fig.add_subplot()

        ax.set_axisbelow(True)

        # Blank out grid
        # ax.grid(linestyle='--', color='gray', zorder=-1)

        # Draw only bottom and left spines; point ticks outward
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='both', which='both', direction='out')
        #     ax.xaxis.set_zorder(3)
        #     ax.yaxis.set_zorder(3)

        # Ticks
        ax.xaxis.set_major_locator(MultipleLocator(x_wid))
        ax.xaxis.set_minor_locator(MultipleLocator(x_wid))
        ax.yaxis.set_major_locator(MultipleLocator(y_wid))
        ax.yaxis.set_minor_locator(MultipleLocator(y_wid))

        # Set limits
        ax.set_xlim(x_min - x_wid_h, x_max + 1.1 * x_wid_h)
        ax.set_ylim(y_min - y_wid_h, y_max + 1.1 * y_wid_h)

        #
        ax.set_aspect('equal')

        #
        # x and y are the center of the box
        xh = x_wid  # * 0.9
        yh = y_wid  # * 0.9
        for i, x in enumerate(np.arange(x_min, x_max + x_wid, x_wid)):
            for j, y in enumerate(np.arange(y_min, y_max + y_wid, y_wid)):
                if ~np.isnan(data[i, j]):
                    color = cmap((data[i, j] - z_min) / (z_max - z_min))
                    ax.add_patch(
                        Rectangle((x - xh / 2., y - yh / 2.), xh, yh, edgecolor='k', facecolor=color, zorder=3))
                    ax.text(x, y, np.round(data[i, j], 2), ha='center', va='center', color='white', size=9)

        # Label axes
        ax.set_xlabel(r'group $i$')
        ax.set_ylabel(r'group $j$')

        fig.savefig('temp.svg')

    heatmap(data, x_min=1, x_max=7, y_min=1, y_max=7)


# Histogram
def hist():
    pass


# Pivot and plot
# TODO support 2D histograms
# TODO right now follows format of pandas -- may change (pivot(x, y, z, bins=blah, zbins=blah)
# TODO should the dependency for iz.pivot be removed?
def pivot(df, index, values, aggfunc='mean', bins=10, show=True):
    xy = iz.pivot(df, index=index, values=values, aggfunc=aggfunc, bins=bins)
    figure = core.figure(style={
        'x_title': index,
        'y_title': values
    })
    figure += core.line(x=xy.index.values, y=xy.iloc[:, 0].values)
    if show:
        figure.show()
    else:
        return figure


# Plot
def plot(data_or_x, y=None, style=None, show=True, **kwargs):
    """
    Create a plot. In most cases, this is the preferred method of interacting with `uplot`.

    Parameters
    ----------
    data_or_x : pandas.DataFrame or ArrayLike
        DataFrame to plot, or the `x` dimension for plotting.
    y : ArrayLike
        (Optional) If present, `y` dimension for plotting.
    style : dict
        If provided, list of style elements.
    show : bool
        Should the figure be shown? (Default: True)
    **kwargs
        Another method to supply style elements.

    Returns
    -------
    matplotlib.pyplot.figure.Figure or None
        Figure or nothing, depending on `show`.
    """

    # Ensure we have a pandas DataFrame from data_or_x
    if isinstance(data_or_x, pd.DataFrame):
        data = data_or_x
    elif isinstance(data_or_x, pd.Series) and y is None:
        data = data_or_x.to_frame()
    elif y is None:
        raise AttributeError('y must be specified')
    else:
        # Format x
        if isinstance(data_or_x, pd.Series):
            x_title = data_or_x.name
            x = data_or_x.to_numpy()
        else:
            x_title = 'x'
            x = data_or_x

        # Format y
        if isinstance(y, pd.Series):
            y_title = y.name
            y = y.to_numpy()
        else:
            y_title = 'y'

        # Create data
        data = pd.DataFrame({x_title: x, y_title: y}).set_index(x_title)

    # Combine style and kwargs
    if style is None:
        style = {}
    style.update(kwargs)

    # Create figure
    # does this need to exclude Line-specific attributes?
    figure = core.figure(data=data, style=style)

    # Start building the figure
    figure += core.line(style={
        'marker': style.get('marker', None),
        'line_style': style.get('line_style', None),
        'line_width': style.get('line_width', None)
    })

    # Return
    if show:
        _ = figure.to_mpl(show=True)
    else:
        return figure.to_mpl(show=False)
