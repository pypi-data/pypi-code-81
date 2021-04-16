import pandas as pd

from jutest.utils.choise import choice
from jutest.utils.display import display


def show_nulls(dataframe: pd.DataFrame, column_name: str = None, **kwargs):
    if column_name is not None:
        column = dataframe[column_name]
        nulls = dataframe[column.isnull()]
    else:
        nulls = dataframe[dataframe.isnull().any(axis=1)]
    nulls = choice(nulls, **kwargs)
    display(nulls, **kwargs)
