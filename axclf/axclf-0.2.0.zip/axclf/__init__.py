"""
axclf

Save/restore Matplotlib axes limits during iterative and interactive
development.

This functionality becomes useful when using cell-mode functionality
in editors such as IdleX, Spyder, IEP, etc. During algorithm prototyping,
plots are generated. These helper routines allow for inspecting a
region of interest on a plot, and then running a change to see its effects
without needing to re-zoom/pan to the region of interest.

Author: Roger D. Serwy

"""

import matplotlib.pyplot as plt
from ._version import __version__


__all__ = ['axclf', 'axrestore', 'AutoClean', '__version__']


def axclf(f=None):
    """Save the active figure's axes limits and clear the figure"""
    if f is None:
        f = plt.gcf()
    axes = f.get_axes()
    limits = []
    for n, a in enumerate(axes):
        x = a.get_xlim()
        y = a.get_ylim()
        limits.append((x,y))
    if not hasattr(f, '__axclf'):
        f.__axclf = limits
    f.clear()


def axrestore(f=None):
    """Restore the axes x and y limits"""
    if f is None:
        f = plt.gcf()
    restore = getattr(f, '__axclf', None)
    if restore is None:
        return
    delattr(f, '__axclf')
    axes = f.get_axes()
    for ax, (x,y) in zip(axes, restore):
        ax.set_xlim(x)
        ax.set_ylim(y)


class AutoClean:
    """Call a clean-up function when the object
       is garbage collected.

       ## Cell
       ac = AutoClean()

       @ac
       def cleanup():
           # when `ac` is re-bound when re-executed
           print('cleaning up')
    """
    def __init__(self):
        self._clean = lambda: None

    def __call__(self, func):
        self._clean = func

    def __del__(self):
        self._clean()

    def clean(self):
        """Execute the clean-up callback and then clears it"""
        func, self._clean = self._clean, lambda: None
        func()
