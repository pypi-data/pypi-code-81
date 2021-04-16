import pandas as pd

from jutest.encode.checker import EncodeChecker
from jutest.utils.choise import choice
from jutest.utils.display import display, warning


def show_encodings(dataframe: pd.DataFrame, encode_checker: EncodeChecker, column_name: str, **kwargs):
    column = dataframe[column_name]
    if column.dtype != 'object':
        warning(f'Column with type "{column.dtype}" cannot have bad encoding')
        return
    mask = column.apply(lambda text: encode_checker.check(text))
    result = dataframe[mask]
    result = choice(result, **kwargs)
    result_samples = result[column_name].apply(lambda text: encode_checker.get_all(text))
    index = dataframe.columns.get_loc(column_name) + 1
    result.insert(index, '[samples]', result_samples)
    display(result, **kwargs)


def _check_encoding(self, column: pd.Series) -> bool:
    for text in column:
        if self.encode_checker.check(text):
            return True
    return False
