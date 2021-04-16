import pandas as pd

from jutest.encode.checker import EncodeChecker
from jutest.settings import NUMBER_DTYPES, DEFAULT_INFO_PRECISION
from jutest.utils.display import display
from jutest.utils.isnan import isnan


class InfoAction:
    def __init__(self, dataframe: pd.DataFrame, encode_checker: EncodeChecker):
        self.dataframe = dataframe
        self.encode_checker = encode_checker

    def info(self, precision: int = DEFAULT_INFO_PRECISION):
        columns, rows = self.dataframe.shape
        memory_usage = self.dataframe.memory_usage(deep=True).sum()
        memory_usage_mb = round(memory_usage / 1024 / 1024, 2)
        display(f'Rows = <b>{columns}</b>, Columns = <b>{rows}</b>, Memory = {memory_usage_mb} Mb', html=True)
        info = list()

        for name in self.dataframe:
            column = self.dataframe[name]
            column_info = ColumnInfo(column, self.encode_checker, precision)
            column_info_data = column_info.info()
            info.append(column_info_data)
        info_df = pd.DataFrame(info, columns=ColumnInfo.INFO_HEADERS)
        display(info_df, full_width=True)


class ColumnInfo:
    INFO_HEADERS = ('name', 'nulls count', 'nulls percent', 'duplicates percent', 'type', 'description', 'encoding')

    def __init__(self, column: pd.Series, encode_checker: EncodeChecker, precision: int = DEFAULT_INFO_PRECISION):
        self.column = column
        self.encode_checker = encode_checker
        self.precision = precision
        self.dtype = self._get_type()

    def info(self) -> tuple:
        basic_info = self._basic_info()
        description = self._description()
        encoding = self._check_encoding() if self.dtype == 'str' else ''
        return basic_info + (self.dtype, description, encoding)

    def _get_type(self) -> str:
        not_nulls = self.column.dropna()
        if len(not_nulls) == 0:
            return 'null'
        dtype = not_nulls.dtype.name
        if dtype == 'object':
            if all(not_nulls.apply(lambda value: isinstance(value, str))):
                dtype = 'str'
            if all(not_nulls.apply(lambda value: isinstance(value, bool))):
                dtype = 'bool'
        if dtype == 'float64':
            if all(not_nulls.apply(lambda value: isnan(value) or value == round(value))):
                dtype = 'int64'
        return dtype

    def _basic_info(self) -> tuple:
        length = self.column.size
        nulls_count = self.column.isnull().sum()
        nulls_percent = round(nulls_count / length * 100, 2)
        unique_count = self.column.nunique(dropna=True) + (nulls_count > 0)
        unique_percent = round((length - unique_count) / length * 100, 2)
        return self.column.name, nulls_count, f'{nulls_percent}%', f'{unique_percent}%'

    def _description(self) -> str:
        column_description = ColumnDescription(self.column, self.dtype, self.precision)
        return column_description.get()

    def _check_encoding(self) -> str:
        for text in self.column:
            if self.encode_checker.check(text):
                return 'Warning'
        return ''


class ColumnDescription:
    def __init__(self, column: pd.Series, dtype: str, precision: int = DEFAULT_INFO_PRECISION):
        self.column = column
        self.dtype = dtype
        self.precision = precision

    def get(self):
        if self.dtype in NUMBER_DTYPES:
            return self.number_description()
        if self.dtype == 'str':
            return self.string_description()
        if self.dtype == 'bool':
            return self.boolean_description()
        if self.dtype == 'null':
            return 'only nulls'
        return ''

    def number_description(self) -> str:
        min_v, max_v, mean, std = self._statistic(self.column)
        if min_v == max_v:
            return f'only {mean}'
        return f'{min_v}-{max_v}, mean={mean}, std={std}'

    def string_description(self) -> str:
        not_nulls = self.column.dropna()
        length_series = not_nulls.apply(len)
        min_v, max_v, mean, std = self._statistic(length_series)
        if min_v == max_v:
            return f'length {int(mean)}'
        return f'length {min_v}-{max_v}, mean={mean}'

    def boolean_description(self) -> str:
        value_counts = self.column.value_counts()
        true = value_counts.get(True, 0)
        false = value_counts.get(False, 0)
        return f'True:{true}, False:{false}'

    def _statistic(self, column: pd.Series):
        min_v = self._round(column.min(), precision=5)
        max_v = self._round(column.max())
        mean = self._round(column.mean())
        std = self._round(column.std())
        return min_v, max_v, mean, std

    def _round(self, value: float, precision: int = None) -> float:
        precision = precision or self.precision
        rounded = round(value, precision)
        if rounded == int(rounded):
            rounded = int(rounded)
        return rounded
