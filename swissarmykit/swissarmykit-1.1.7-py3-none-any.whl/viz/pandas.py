import json
import numpy as np
import pandas as pd
from datetime import datetime

try: from definitions_prod import swissarmykit_conf
except Exception as e: pass

from pandas import Series, DataFrame
from swissarmykit.lib.baseobject import BaseObject
from swissarmykit.utils.fileutils import FileUtils
from swissarmykit.utils.dateutils import DateUtils
from swissarmykit.viz.Seaborn import Seaborn


class Pandas(Seaborn, BaseObject):
    '''
    No extend DataFrame, because it's too large, and can't override core function.

    Docs:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html

    from swissarmykit.viz.pandas import Pandas

    '''

    df: DataFrame

    def __init__(self, df=None, index=None, columns=None, dtype=None, copy=False):

        if isinstance(df, DataFrame):
            self.df = df
        elif isinstance(df, pd.Series):
            self.df = pd.DataFrame(df, index=index, columns=columns, dtype=dtype, copy=copy)
        elif isinstance(df, dict) or isinstance(df, list):
            self.df = pd.DataFrame(df, index=index, columns=columns, dtype=dtype, copy=copy)
        elif isinstance(df, str):
            df = df.strip()
            if df[0] in ['[', '{']:
                self.df = pd.DataFrame(json.loads(df))
            else:
                ext = df.rsplit('.', 1)[-1]
                if ext.startswith('xl'):
                    ext = 'excel'
                self.df = getattr(pd, 'read_' + ext)(df)
    
        super().__init__(self.df)
        self._object = self.df

    def isnull(self):
        return Pandas(self.df.isnull())

    def get_columns(self):
        ''' https://stackoverflow.com/questions/24870306/how-to-check-if-a-column-exists-in-pandas '''
        return self.df.columns.tolist()

    def set_columns(self, cols):
        self.df.columns = cols

    def notnull(self):
        return Pandas(self.df.notnull())

    def transpose(self):
        return Pandas(self.df.T)

    def fill_nan(self, value, series_col=None):
        ''' Fill NA/NaN values using the specified method.
            series_col: str or list of cols
        '''
        if series_col:
            series_col = series_col if isinstance(series_col, list) else [series_col]
            if set(series_col).issubset(self.df.columns):
                self.df[series_col] = self.df.loc[:,series_col].fillna(value=value)
            else:
                print('WARN: Not exists this columns: ', set(series_col).difference(self.df.columns), ' in this df.columns: ', self.get_columns())
        else:
            self.df.fillna(value=value, inplace=True)
        return self

    def sort_by_index(self, axis=0, ascending=True):
        self.df.sort_index(axis, ascending=ascending)
        return self

    def sort_by_values(self, by, axis=0, ascending=True):
        self.df.sort_values(by, axis=axis, ascending=ascending)
        return self

    def index(self, lst):
        self.df.set_index(lst)
        return self

    def get_column(self, name):
        return Pandas(self.df[name])

    def get_row(self, name) -> 'Pandas':
        return Pandas(self.df.loc[name])

    def get_total(self):
        return self.df.shape[0]

    def get_series(self, name: str) -> Series:
        return self.df[name]

    def value_counts(self, fillna=0):
        ''' Same as rank '''
        return Pandas(self.df.apply(pd.value_counts).fillna(fillna))

    def get_dict(self, cols):
        ''' cols=[index, value] => {} '''
        return pd.Series(self.df[cols[1]].values, index=self.df[cols[0]]).to_dict()

    def map(self, col_name, with_df:BaseObject, on_cols, new_col=None, fillna=''):
        ''' https://stackoverflow.com/questions/20250771/remap-values-in-pandas-column-with-a-dict '''

        _s = pd.Series(with_df.df[on_cols[1]].values, index=with_df.df[on_cols[0]])
        self.df[new_col if new_col else col_name] = self.df[col_name].map(_s).fillna(fillna)
        return self

    def to_numeric(self, cols=None):
        return self.convert_to_type(cols, dtype=pd.to_numeric)

    def to_datetime(self, cols=None, new_cols=None, unit=None, errors='coerce'):
        if new_cols:
            self.df[new_cols] = self.df[cols].apply(pd.to_datetime, errors=errors)
        else:
            self.df[cols] = self.df[cols].apply(pd.to_datetime, errors=errors)

        if unit:
            self.df[new_cols if new_cols else cols] = self.df[cols].apply(lambda x: x.year)

        return self

    def to_timedelta(self, cols=None, unit=None, now=None, new_cols=None, errors='coerce'):
        ''' D M Y h m s'''

        unit = unit.lower() if unit and unit not in ['m'] else unit
        if not now: now = pd.datetime.now()
        cols = cols if isinstance(cols, list) else [cols]
        new_cols = new_cols if isinstance(new_cols, list) else [new_cols]

        _unit = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'M': 18144000, 'y': 31536000}

        print(f'INFO: Convert cols: {cols} to {unit}. now: {now} )')
        for i, col in enumerate(cols):
            if isinstance(self.df[col][0], str):
                print(f'WARN: this column not datetime yet. Auto convert p.to_datetime("{col}")')

                _s = self.df[col].apply(pd.to_datetime, errors=errors)
            else:
                _s = self.df[col]


            if unit:
                self.df[col if not new_cols else new_cols[i]] = (now - _s).dt.total_seconds() / _unit.get(unit, unit)
            else:
                self.df[col if not new_cols else new_cols[i]] = now - _s

        return self

    def convert_to_type(self, cols=None, new_cols=None, dtype=pd.to_numeric):
        ''' If None, convert all cols to numeric. Or select specific columns '''
        if cols:
            cols = cols if isinstance(cols, list) else [cols]
            if new_cols:
                self.df[new_cols] = self.df[cols].apply(dtype)
            else:
                self.df[cols] = self.df[cols].apply(dtype)
        else:
            self.df.apply(dtype)

        return self

    def get_list(self, add_col=False, as_string=False):
        re = ([self.df.columns.values.tolist()] if add_col else []) + self.df.values.tolist()

        if as_string:
            index = re.pop(0) if add_col else None
            re = 'Pandas(%s, columns=%s)' % (str(re), str(index))

        return re

    def apply_fx(self, cols=None, fx=None, inplace=False):
        _s = self.df[cols].apply(fx) if hasattr(fx, '__call__') else (self.df[cols] + fx)

        if inplace:
            self.df.update(_s)
        else:
            _df = self.df.copy()
            _df[cols] = _s
            return Pandas(_df)

        return self

    def apply_func(self, func, cols=None):
        self.df[cols] = func(self.df)
        return self

    def get_obj_as_str(self):
        return self.get_list(add_col=True, as_string=True)

    def __getitem__(self, item):
        return Pandas(super().__getitem__(item))

    def filters(self, cols, condition):
        '''


        :param cols:
        :param condition:
        :return:
        '''
        df = self.df[self.df[cols[0]].eq(condition)]
        return Pandas(df)

    def query_by(self, expr=None, filters=None, filter_out_nan=None, to_datetime=None):
        ''' Ref:
                    https://cmdlinetips.com/2019/07/how-to-select-rows-of-pandas-dataframe-with-query-function/
                    https://docs.mongoengine.org/guide/querying.html#query-operators
                    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html
            :param filters col_name__== or __>= or __<  or __!=
         '''
        if filters:
            lst = []
            _op = {'eq': '==', 'ne': '!=', 'lt': '<', 'lte': 'lte', 'gt': '>', 'gte': '>='}
            dtypes = self.df.dtypes

            for k, v in filters.items():
                if '__' not in str(k):
                    op = '=='
                else:
                    k, op = k.split('__')
                    op = _op.get(op, op)

                if type(v) in [datetime, pd._libs.tslibs.timestamps.Timestamp]:
                    v = str(v).split(' ')[0].replace('-', '')
                    
                lst.append('%s %s %s' % (k, op, '"%s"' % v if isinstance(v, str) else v))

            expr = ' & '.join(lst)
            # print(expr)

        if to_datetime:
            self.to_datetime(to_datetime, errors='coerce')

        if filter_out_nan:
            df = self.df.query(expr)
            p = Pandas(df[df[filter_out_nan].notnull().all(1)])
        else:
            p = Pandas(self.df.query(expr))

        return p

    def filter_out_nan(self, cols=None):
        ''' https://stackoverflow.com/questions/22551403/python-pandas-filtering-out-nan-from-a-data-selection-of-a-column-of-strings '''
        if cols:
            return Pandas(self.df[self.df[cols].notnull().all(1)])

        return Pandas(self.df.dropna(thresh=2))

    def copy(self):
        return Pandas(self.df.copy())

    def less(self, max_rows=5, max_cols=30, precision=2):
        s = self.df.shape
        print(f'Rows: {s[0]} - Columns: {s[1]}\n\nColumn Names: {self.df.columns}\n\ndtypes: {self.df.dtypes}\n')
        print(self.df.describe())
        with pd.option_context('display.max_rows', None, 'display.max_columns', max_cols, 'max_colwidth', 30, 'precision', precision):
            print(self.df[:max_rows])


    def is_empty(self):
        return self.df.empty

    @staticmethod
    def series(lst:any, index:list=None):
        if index:
            return pd.Series(lst, index)
        return pd.Series(lst)

    def save_checkpoint(self, name=None):
        ''' https://stackoverflow.com/questions/17098654/how-to-store-a-dataframe-using-pandas '''

        if not name:
            name = BaseObject.get_variable_name(self)
        name = FileUtils._get_pickle_path(name)
        self.df.to_pickle(name)
        print('INFO: to_pick ', name)

    def output_to_excel(self, file_name=None, format='xlsx'):
        _format = {'xlsx': 'to_excel', 'csv': 'to_csv'}

        if not file_name: file_name = FileUtils._get_file_path(self.get_cls_name(), format)
        file_name = FileUtils._get_file_path(file_name, format)

        output = getattr(self.df, _format.get(format))
        try:
            output(file_name)
        except Exception as e:
            print(e)
            output(file_name + str(datetime.now()) + '.' + format)

    def output_to_csv(self, file_name=None, format='csv'):
        self.output_to_excel(file_name=file_name, format=format)

    @staticmethod
    def load_checkpoint(name):
        name = FileUtils._get_pickle_path(name)
        return Pandas(pd.read_pickle(name))

    @staticmethod
    def get_NaN():
        return pd.np.nan

    def dump(self, name=None):
        self.save_checkpoint(name=name)

    def get_one(self, limit=1, offset=0, filters=None):
        ''' loc[rows, columns] used label, iloc[rows, columns] use index'''
        if filters:
            return Pandas(self.query_by(filters=filters)[offset:limit])
        return Pandas(self.df[offset:limit])

    def iter_(self):
        ''' https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/ '''
        df = self.df
        for index, row in df.iterrows():
            print (row["Name"], row["Age"])

    def get_value_fx(self, x, y, value):
        ''' Used to find y = f(x) '''
        y_index =  self.df[x][self.df[x] >= value].index[0]
        return self.df[y][y_index]

    def get_row_by(self, by, value, cols=None):
        row = self.df[by][self.df[by] == value]
        if not row.empty:
            if cols:
                return self.df.iloc[row.index[0], cols]
            return self.iloc[row.index[0]]
        return pd.Series([])

    def attention_formula(self, zoom = 5):

        df = self.df
        # Ratio of views/likes = 30, 20. attention have great ratio than views.
        magnify = pd.Series(np.ones((df.shape[0], )))  # Range: 1 => 99. To magnify attention.
        attention = pd.Series(np.ones((df.shape[0], )))  # Range: 1 => 99. To magnify attention.

        likes = df['like']
        dislikes = df['dislike']

        lr = likes * 100 / (likes + dislikes)  # like ratio: abbr: lr. unit: 1%-100%
        dr = dislikes * 100 / (likes + dislikes)  # dislike ratio: abbr: dr. unit: 1%-100%

        # So good: 900 likes, 100 dislikes. 90%, 10%
        magnify = magnify.where(lr.ge(0.8) & (lr / dr).ge(dr), lr * zoom / dr)\
            .where(dr.ge(lr / 2), dr**2 * 100 * zoom)  # Abnormal: 35 > 65 / 2.  dislikes %: 35,40,50,60


        # Normal: 80/20
        p80_20 = (lr / 4).ge(dr)
        attention = attention.where(p80_20, abs(likes - dislikes) * magnify).where(~p80_20,  (likes + dislikes) * magnify)

        cols = ['magnify', 'attention', 'attention_diff', 'like_ratio']

        df['magnify'] = magnify
        df['attention'] = attention + df['views']
        df['attention_diff'] = df['attention'] - df['views']
        df['like_ratio'] = lr

        self.fill_nan(0, series_col=cols)
        return cols

    def youtube_magnify(self):
        pass

if __name__ == '__main__':
    # data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
    #         'year': [2000, 2001, 2002, 2001, 2002, 2003],
    #         'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
    # p = pd.DataFrame(data)
    #
    # print(type(p['state']))
    #
    # data2 = [['a', 'apple'], ['b', 'banana']]
    # p2 = Pandas(data2)

    # print(type(p2.df[0]))


    # df_train = Pandas(swissarmykit_conf.EXCEL_PATH + '/ytvideo.csv')
    # pchannel = Pandas(swissarmykit_conf.EXCEL_PATH + '/ytchannel.csv')
    # pcategory = Pandas(swissarmykit_conf.EXCEL_PATH + '/note_category.csv')
    # print(pchannel)
    # print(pchannel.fill_nan('', 'parent'))
    # print(pchannel.to_datetime('joinedDate')[:3])
    # print(pchannel._object)
    # print(type(pchannel.to_datetime('joinedDate')[:3]))
    # print(pchannel.to_datetime('joinedDate').less())

    p = Pandas(swissarmykit_conf.EXCEL_PATH + '/ytvideo.csv')
    p1 = p.query_by(filters={'channelId': 'UCzQUP1qoWDoEbmsQxvdjxgQ', 'views__<=': 2e6, 'published_date__>=': '2013-01-01'},
                    filter_out_nan=['published_date', 'views'], to_datetime=['published_date'])

    p1.attention_formula(5)
    # p1.to_timedelta('published_date', unit='h', new_cols='date')
    # data = p1.plot('date', y='attention', kind='lm')


    # p1.output_to_excel()
    p1.dump()
    print(p1.less())

    # p1.output_to_excel('JoeRogan')
    # p.save_checkpoint('test')
    # p = Pandas.load_checkpoint('test')

    # p = Pandas(swissarmykit_conf.DIST_PATH + '/xlsx/Pandas.xlsx')
    # p.to_datetime('published_date', 'date')
    # p.to_timedelta('date', 'd')
    # p = p.filter_out_nan(['published_date', 'views'])
    # print(p.less())

    # timestamp = pd.Series(['34:23', '125:26', '15234:52'])
    # x = timestamp.str.split(":").apply(lambda x: int(x[0]) * 60 + int(x[1]))
    # timestamp = pd.to_timedelta(x, unit='s')
    # print(timestamp)
    # data = [[1, 'a'], [2, 'b'], [4, 'd'], [4, 'a'], [4, 'f'], ]
    # p = Pandas(data)
    # p.set_columns(['a', 'b'])

    # p = Pandas(swissarmykit_conf.DIST_PATH + '/Book1.xlsx')
    # print(p)
    # print(p.get_columns())
    # print(p.df.query('b=="a"'))
    # print(p.query_by(filters={'a': 'a'}).is_empty())
    # print(Pandas.load_checkpoint('p'))

    # print(p.map(1, p2, [0, 1], 'new_col'))
    # print(p.to_numeric([0]))
    # print(p.get_list(False, True))


    # print(p)
    # print(p.columns)
    # print(p.get_series('state'))

    # print(p.series([4, 7, -5, 3],index=['d', 'b', 'a', 'c']))

