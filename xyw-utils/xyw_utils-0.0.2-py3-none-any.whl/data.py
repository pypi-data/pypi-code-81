from inspect import isfunction
from functools import wraps
import re
import math
import pandas as pd
import numpy as np
from scipy import interpolate
from scipy.integrate import simps
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from xyw_utils.path import FileName


class ExcelModel:
    """
    excel文件读写模块
    """
    @staticmethod
    def read(io, sheet_name=0, header=0, names=None, usecols=None, dtype=None):
        if usecols is not None and names is not None and len(usecols) != len(names):
            raise ValueError('too many columns specified:expected %d and found %d' % (len(usecols), len(names)))
        df = pd.read_excel(io, sheet_name=sheet_name, usecols=usecols, header=header)
        if usecols is not None:
            usecols = [df.columns[item] if isinstance(item, int) else item for item in usecols]
            df = df[usecols]
        if names is not None:
            rename_dict = dict(zip(df.columns, names))
            df = df.rename(columns=rename_dict)
        if dtype is not None:
            if not isinstance(dtype, dict):
                raise TypeError('param dtype must be dict')
            for key, value in dtype.items():
                if isfunction(value):
                    df[key] = df[key].apply(value)
                elif isinstance(value, str):
                    df[key] = df[key].astype(value)
                else:
                    raise TypeError('param dtype must be dict-like of function or str')
        return df

    @staticmethod
    def write(df, io, sheet_name='Sheet1', index=False):
        df.to_excel(io, sheet_name=sheet_name, index=index)


class CsvModel:
    """
    csv文件读写模块
    """
    @staticmethod
    def read(io, header=0, names=None, usecols=None, dtype=None):
        if usecols is not None and names is not None and len(usecols) != len(names):
            raise ValueError('too many columns specified:expected %d and found %d' % (len(usecols), len(names)))
        df = pd.read_csv(io, usecols=usecols, header=header)
        if usecols is not None:
            usecols = [df.columns[item] if isinstance(item, int) else item for item in usecols]
            df = df[usecols]
        if names is not None:
            rename_dict = dict(zip(df.columns, names))
            df = df.rename(columns=rename_dict)
        if dtype is not None:
            if not isinstance(dtype, dict):
                raise TypeError('param dtype must be dict')
            for key, value in dtype.items():
                if isfunction(value):
                    df[key] = df[key].apply(value)
                elif isinstance(value, str):
                    df[key] = df[key].astype(value)
                else:
                    raise TypeError('param dtype must be dict-like of function or str')
        return df

    @staticmethod
    def write(df, io, index=False):
        df.to_csv(io, index=index)


class FileProcessorFacade:
    """
    文件读写的外观类
    """
    def __init__(self):
        self.__excel_model = ExcelModel()
        self.__csv_model = CsvModel()

    def read(self, io, sheet_name=0, header=0, names=None, usecols=None, dtype=None):
        if not isinstance(io, str):
            raise TypeError('param io must be string')
        file = FileName(io)
        if file.is_ext(['.xlsx', '.xls']):
            return self.__excel_model.read(
                file.fullpath, sheet_name=sheet_name, header=header,
                names=names, usecols=usecols, dtype=dtype,
            )
        elif file.is_ext('.csv'):
            return self.__csv_model.read(
                file.fullpath, header=header, names=names,
                usecols=usecols, dtype=dtype,
            )
        else:
            raise ValueError('unsupport file type')

    def write(self, df, io, sheet_name='Sheet1'):
        file = FileName(io)
        if file.is_ext(['.xlsx', '.xls']):
            file.make_dir()
            self.__excel_model.write(df, file.fullpath, sheet_name=sheet_name)
        elif file.is_ext('.csv'):
            file.make_dir()
            self.__csv_model.write(df, file.fullpath)
        else:
            raise ValueError('unsupport file type')


def validate_df(func):
    """
    判断参数是否为pandas中DataFrame类型的装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if isinstance(args[0], pd.DataFrame):
            # 将第一个df参数替换为其复制
            args = list(args)
            args[0] = args[0].copy()
            return func(*args, **kwargs)
        else:
            raise TypeError('support pandas.DataFrame only')
    return wrapper


def validate_dfs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        if isinstance(args[0], list):
            for item in args[0]:
                if not isinstance(item, pd.DataFrame):
                    raise TypeError('support list of pandas.DataFrame only')
        else:
            raise TypeError('support list of pandas.DataFrame only')
        args[0] = [item.copy() for item in args[0]]
        return func(*args, **kwargs)
    return wrapper


@validate_df
def remove_unnamed(df):
    """
    移除df中的Unnamed列
    :param df:
    :return:
    """
    pattern = re.compile(r'^Unnamed: \d*$')
    unnamed = [item for item in df.columns if pattern.match(item)]
    return df.drop(columns=unnamed)


@validate_df
def remove_nan(df):
    """
    移除df中有无效值的行
    :param df:
    :return:
    """
    return df.dropna(axis=0, how='any').reset_index(drop=True)


@validate_df
def init_split(df):
    """
    单独时间列df数据的初始化
    :param df:
    :return:
    """
    df = remove_unnamed(df)
    if df.shape[1] % 2:
        raise RuntimeError('columns of the df is not an even number')
    pattern = re.compile(r'^(.*)\.\d*$')
    res = []
    for i in range(df.shape[1] // 2):
        tem = df.iloc[:, [i*2, i*2+1]]
        tem = remove_nan(tem)
        match_res = pattern.match(tem.columns[0])
        if match_res:
            tem.rename(columns={tem.columns[0]: match_res.group(1)}, inplace=True)
        res.append(tem)
    return res


@validate_df
def init_merged(df):
    """
    唯一时间列df数据的初始化
    :param df:
    :return:
    """
    df = remove_unnamed(df)
    res = []
    for i in range(df.shape[1] - 1):
        tem = df.iloc[:, [0, i+1]]
        tem = remove_nan(tem)
        res.append(tem)
    return res


@validate_df
def set_zero(df):
    """
    将df数据的第一列起始值归零
    :param df:
    :return:
    """
    df.iloc[:, 0] = df.iloc[:, 0] - df.iloc[0, 0]
    return df


@validate_df
def resample_single(df, step=0.01, kind=None):
    """
    重采样
    :param df: 两列的df数据，第一列一般为时间列
    :param step: 采样步长
    :param kind: 插值方法
    :return:
    """
    if kind is None:
        kind = 'linear'
    if df.shape[1] != 2:
        raise RuntimeError('the number of columns must be two')
    f = interpolate.interp1d(df.iloc[:, 0], df.iloc[:, 1], kind=kind)
    start = math.ceil(df.iloc[0, 0] / step)
    end = math.floor(df.iloc[-1, 0] / step)
    x = np.arange(start, end + 1, step=1, dtype=int)
    x = x * step
    y = f(x)
    return pd.DataFrame(np.vstack((x, y)).T, columns=df.columns)


@validate_df
def get_derivation(df, method='grad'):
    """
    离散数据求导
    :param df:
    :param method: 微分方法，diff方法下第一行数据为NAN
    :return:
    """
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]
    # 中心差分法
    if method == 'grad':
        dx = np.gradient(x)
        dy = np.gradient(y)
    # 向前差分法
    elif method == 'diff':
        dx = x.diff()
        dy = y.diff()
    else:
        raise ValueError('not support such method, grad and diff only')
    res = dy / dx
    name = method + '[' + x.name + ',' + y.name + ']'
    res = pd.Series(res, name=name)
    return res


@validate_df
def get_integral(df, method='trapz'):
    """
    离散数据求积分
    :param df:
    :param method: 积分方法
    :return:
    """
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]
    # 辛普森法
    if method == 'simps':
        res = [simps(y[0:i+1], x[0:i+1]) for i in range(len(x))]
    # 复杂梯形法
    elif method == 'trapz':
        res = [np.trapz(y[0:i+1], x[0:i+1]) for i in range(len(x))]
    else:
        raise ValueError('not support such method, simps and trapz only')
    name = method + '[' + x.name + ',' + y.name + ']'
    res = pd.Series(res, name=name)
    return res


@validate_dfs
def resample_all(dfs, step=0.01, kind=None):
    """
    将列表中的df统一重采样
    :param dfs:
    :param step:
    :param kind:
    :return:
    """
    return [resample_single(item, step=step, kind=kind) for item in dfs]


@validate_dfs
def merge_all(dfs, drop_nan=True, zero=False):
    """
    将列表中的多个df拼接为一个df
    :param drop_nan: 是否删除有nan的行
    :param dfs:
    :param zero: 是否将第一列初始值归零
    :return:
    """
    res = dfs[0]
    name = res.columns[0]
    for i in range(len(dfs)-1):
        res = pd.merge(res, dfs[i+1], how='outer', on=name)
    if drop_nan:
        res = remove_nan(res)
    res = res.sort_values(by=name, ascending=True).reset_index(drop=True)
    if zero:
        res = set_zero(res)
    return res


@validate_df
def get_local_outlier_factor(df, k):
    """
    计算局部离群因子值
    :param df:
    :param k: 取离样本点p第k个最近的距离
    :return:
    """
    # def f1(x, df, k):
    #     tem = np.sqrt(((df - x) ** 2).sum(axis=1))
    #     tem = tem.sort_values()
    #     return 1 / tem.iat[k], tem.iloc[1:k + 1].index
    #
    # def f2(x, df):
    #     tem = df[0][x[1]].mean()
    #     return tem / x[0]

    if not isinstance(k, int):
        raise TypeError('param k must be int')
    if len(df) < k+1:
        raise RuntimeError('param k must be smaller than the length of df')

    name = 'lof' + str(list(df.columns))

    # df = df.reset_index(drop=True)
    # df = df.apply(f1, axis=1, args=(df, k)).apply(pd.Series)
    # res = df.apply(f2, axis=1, args=(df,))
    # res.name = name
    # return res

    rho = []
    index = []
    for i in range(len(df)):
        tem = np.sqrt(((df - df.iloc[i, :])**2).sum(axis=1))
        tem = tem.sort_values()
        rho.append(1 / tem.iat[k])
        index.append(tem.iloc[1:k+1].index)
    rho = pd.Series(rho)
    res = []
    for i in range(len(df)):
        tem = rho[index[i]].mean()
        res.append(tem / rho[i])
    res = pd.Series(res, name=name)
    return res


@validate_df
def remove_outlier(df, contamination=0.01, k=20):
    """
    移除数据中离群点所在行
    :param df:
    :param contamination: 离群点比例
    :param k: 局部离群因子算法中的k
    :return:
    """
    tem = get_local_outlier_factor(df, k=k)
    tem = tem.sort_values(ascending=False)
    contamination = math.ceil(len(df)*contamination)
    index = list(tem.iloc[0:contamination].index)
    df.iloc[index, :] = np.nan
    df = remove_nan(df)
    return df


@validate_df
def get_linear_fitting(df, method):
    """
    常用最小二乘法线性拟合
    :param df:
    :param method:
    :return:
    """
    # 无常数项一次拟合
    def fun1(x, a):
        return a * x

    # 无常数项二次拟合
    def fun2(x, a, b):
        return a * x ** 2 + b * x

    # 无常数项三次拟合
    def fun3(x, a, b, c):
        return a * x ** 3 + b * x ** 2 + c * x

    x = df.iloc[:, 0]
    y = df.iloc[:, 1]

    if method in [1, 2, 3]:
        popt = np.polyfit(x, y, method)
    elif method == 4:
        popt, _ = curve_fit(fun1, x, y)
        popt = np.append(popt, 0)
    elif method == 5:
        popt, _ = curve_fit(fun2, x, y)
        popt = np.append(popt, 0)
    elif method == 6:
        popt, _ = curve_fit(fun3, x, y)
        popt = np.append(popt, 0)
    else:
        raise ValueError('param method must be int between 1 and 6')
    return np.poly1d(popt)


@validate_df
def plot(df):
    p = plt.plot(df.iloc[:, 0], df.iloc[:, 1])
    plt.show()
    return p


if __name__ == '__main__':
    # from io import StringIO, BytesIO
    # import os
    #
    # data = ('col1,col2,col3\n'
    #         'a,b,1\n'
    #         'a,b,2\n'
    #         'c,d,3')
    #
    # usercols = [2, 0]
    # names = ['x', 'y']
    # header = None
    #
    # reader = CsvModel()
    # reader2 = FileProcessorFacade()
    # df = reader.read(StringIO(data), usecols=[2, 1, 0], names=['x', 'y', 'z'])
    # # df = reader.read(StringIO(data), usecols=[1, 0], names=['x', 'y'], dtype={'x': lambda x: x == 'b'})
    #
    # # df = pd.read_csv(StringIO(data), usecols=[1, 0], names=['x', 'y'], header=1, dtype={'x': bool})
    # print(df)
    # print(df.dtypes)
    #
    # reader2.write(df, os.path.join('xue', 'x.csv'))
    processor = FileProcessorFacade()
    # df = processor.read(r'C:\Users\Administrator\Desktop\JS6108GHBEV31\65%载荷\ZZ-CCBC-65%-1.csv', sheet_name=2)
    df = processor.read(r'C:\Users\Administrator\Desktop\cw\wthz-l-1.xlsx', sheet_name=2)
    # df = processor.read(r'1.xlsx', sheet_name=2)
    dfs = init_merged(df)
    df = resample_single(dfs[0], step=0.01)
    re = get_integral(df)
    # df2 = resample_all(dfs, step=0.1)
    # df2 = merge_all(df2)
    # df = init_split(df)
    print(df)
