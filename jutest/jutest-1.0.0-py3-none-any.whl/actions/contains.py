import pandas as pd

from jutest.utils.choise import choice
from jutest.utils.display import display


class ContainsAction:
    def __init__(self, filename: str):
        self.file_data = self._load_file(filename)

    @staticmethod
    def _load_file(filename: str) -> set:
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
            return set(lines)

    def contains(self, dataframe: pd.DataFrame, column_name: str, **kwargs):
        column = dataframe[column_name]
        data = set(column)

        missing = self.file_data - data
        redundant = data - self.file_data

        self._display(missing, 'missing', **kwargs)
        display('<br>', html=True)
        self._display(redundant, 'redundant', **kwargs)

    @staticmethod
    def _display(values: set, title: str, full_width: bool = True, **kwargs):
        if len(values) > 0:
            values = pd.Series(list(values), name=title)
            values_display = choice(values, **kwargs)
            display(f'There is <b>{len(values)}</b> {title} values:', html=True)
            display(values_display, full_width=full_width, **kwargs)
        else:
            display(f'No {title} values', html=True)
