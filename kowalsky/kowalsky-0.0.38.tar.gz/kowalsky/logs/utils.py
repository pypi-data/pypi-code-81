import matplotlib.pyplot as plt
import pylab as pl
from IPython import display
import math
import sys


def calc_percent(part, all):
    return f"{round(part / all * 100)}%"


def make_pretty_pyplot():
    plt.style.use('ggplot')


def sizeof_format(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def profile_memory(n_first=10):
    items = [(name, sys.getsizeof(value)) for name, value in globals().items()]

    sorted_items = sorted(items, key=lambda x: -x[1])
    for name, size in sorted_items[:n_first]:
        print("{:>30}: {:>8}".format(name, sizeof_format(size)))

    names, sizes = zip(*items)
    print("\n{:>30}: {:>8}".format('ALL', sizeof_format(sum(sizes))))


class LivePyPlot:

    def __init__(self, direction, show_true_value=False):
        self.x = []
        self.y = []
        self.best = -math.inf if direction == 'maximize' else math.inf
        self.fn = max if direction == 'maximize' else min
        self.show_true_value = show_true_value

    def __call__(self, new_point, x=None):
        self.best = self.fn(new_point, self.best)
        self.y.append(self.best if not self.show_true_value else new_point)
        self.x.append(x if x is not None else len(self.y))

        plt.title(f"Best: {self.best:.3f}")
        plt.plot(self.x, self.y, color='red')

        display.clear_output(wait=True)
        display.display(pl.gcf())

    def clear(self):
        plt.close()
