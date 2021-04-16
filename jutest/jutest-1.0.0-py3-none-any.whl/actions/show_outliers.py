import pandas as pd

from jutest.settings import NUMBER_DTYPES
from jutest.utils.choise import choice
from jutest.utils.display import display, warning


def show_outliers(dataframe: pd.DataFrame, column_name: str, **kwargs):
    column = dataframe[column_name]
    if column.dtype not in NUMBER_DTYPES:
        warning(f'Column with type "{column.dtype}" cannot have outliers')
        return
    mean = column.mean()
    std = column.std()
    outliers = dataframe[(column > mean + 3 * std) | (column < mean - 3 * std)]
    outliers = choice(outliers, **kwargs)
    display(outliers, **kwargs)
