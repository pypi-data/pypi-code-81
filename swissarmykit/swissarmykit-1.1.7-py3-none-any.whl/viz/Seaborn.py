import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import seaborn as sns

from swissarmykit.lib.baseobject import BaseObject

try:
    from definitions_prod import *
except Exception as e:
    pass


class Seaborn(BaseObject):
    df: DataFrame

    def __init__(self, df):
        super().__init__(df)
        self._plt = sns

    def get_seaborn(self):
        return self._plt

    def plot(self, x=None, y=None, dir='up', value=None, inplace=False, height=5, aspect=2, kind='line'):
        '''
         General graph.

        :param x: horizon
        :param y: vertical
        :param size: small (s), medium (m), large (l), super (x), or (width, height)
        :param dir: up, down, left, right
        :param value: numeric, f(x)
        :param kind: line, scatter, dist
        :return: graph

        '''

        p = self
        line = 0
        if value:
            if dir in ['up', 'down']:
                p = self.apply_fx(y, value if dir == 'up' else -1 * value, inplace=inplace)
            else:
                p = self.apply_fx(x, -1 * value if dir == 'right' else value, inplace=inplace)


        if kind in ['line', 'scatter']:
            from pandas.plotting import register_matplotlib_converters
            register_matplotlib_converters()
            g = sns.relplot(x=x, y=y, kind=kind, data=p.df, height=height, aspect=aspect)
            g.fig.autofmt_xdate()


            # Issue: https://github.com/mwaskom/seaborn/issues/1641  datetime auto-scale
            if pd.core.dtypes.common.is_datetime_or_timedelta_dtype(p.df[x]):
                g.set(xlim=(p.df[x].min(), p.df[x].max()))

        elif kind in ['dist']:
            g = sns.distplot(p.df[x if x else y], vertical=False if x else True)
        elif kind in ['ts']:
            g = sns.lineplot(x=x, y=y, data=p.df)
        elif kind in ['lm']:
            # https://stackoverflow.com/questions/46248348/seaborn-matplotlib-how-to-access-line-values-in-facetgrid
            g = sns.lmplot(x=x, y=y, data=p.df, order=2, ci=None, scatter_kws={"s": 10}, height=height, aspect=aspect)
            plt.show()

            line = g.axes.flat[0].lines[0]
            data = {'x': pd.Series(line.get_xdata()), 'y': pd.Series(line.get_ydata())}

            # print(p)
            return data

        else:
            print(f'WARN: Unknown kind {kind}')

        plt.show()

    def example(self):

        pass


if __name__ == '__main__':

    # p.plot('Date', 'Views', value=100, kind='scatter', inplace=True)
    # print(p)

    # print(p.plot('Date', 'Views', kind='scatter'))
    # print(p.plot('Date', 'Views', value=np.log, kind='scatter'))
    p = Pandas.load_checkpoint('p1')
    p.to_timedelta('published_date', unit='h', new_cols='date')
    # p.to_datetime('published_date')
    data = p.plot('date', y='attention', kind='lm')
    # d = Pandas(data)
    # print(d.get_value_fx('x', 'y', 2015))

    # print(p.plot('published_date', y='attention', kind='scatter'))
    # print(p.plot('attention', kind='dist'))
    # print(p)
