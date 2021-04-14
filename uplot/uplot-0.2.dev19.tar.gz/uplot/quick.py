"""
quick.py
Written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from . import core

import izzy as iz
import pandas as pd
from typelike import ArrayLike


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
    elif y is None:
        raise AttributeError('y must be specified')
    else:
        # Add x
        if isinstance(data_or_x, pd.Series):
            data = data_or_x.to_frame()
        else:
            data = pd.DataFrame({'x': data_or_x})

        # Add y
        if isinstance(y, pd.Series):
            data[y.name] = y
        else:
            data['y'] = y

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
