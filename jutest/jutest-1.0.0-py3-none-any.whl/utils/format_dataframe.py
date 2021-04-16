import pandas as pd

from jutest.settings import DISPLAY_MAX_TEXT_LENGTH
from jutest.utils.isnan import isnan

NONE_TEMPLATE = '<p style="color:red;">nan</p>'


class FormatDataFrame:
    def __init__(self, dataframe: pd.DataFrame):
        self._dataframe = dataframe
        self._full_width = False
        self._clickable = False

    def format(self, full_width: bool = False, clickable: bool = True, **kwargs):
        self._full_width = full_width
        self._clickable = clickable
        data = self._dataframe.style
        for name in self._dataframe.columns:
            column = self._dataframe[name]
            if not self._is_only_links(column):
                data = data.format({name: self._format})
            else:
                data = data.format({name: self._format_clickable})
        return data

    @staticmethod
    def _is_only_links(series: pd.Series) -> bool:
        if series.dtype != 'object':
            return False
        not_nulls = 0
        for value in series:
            if isinstance(value, str):
                if not value.startswith('http') or ' ' in value.strip():
                    return False
            not_nulls += 1
        return not_nulls > 0

    def _format(self, value):
        if isnan(value):
            return NONE_TEMPLATE
        if isinstance(value, str) and not self._full_width:
            value = value.replace('&', '&amp;')
            return self._truncate(value)
        else:
            return value

    def _format_clickable(self, value):
        text_value = self._format(value)
        if isinstance(value, str):
            return self._make_clickable(value, text_value)
        else:
            return text_value

    @staticmethod
    def _truncate(value: str) -> str:
        if len(value) > DISPLAY_MAX_TEXT_LENGTH + 1:
            return value[:DISPLAY_MAX_TEXT_LENGTH] + '...'
        return value

    @staticmethod
    def _make_clickable(value: str, text_value: str) -> str:
        return f'<a href="{value}">{text_value}</a>'
