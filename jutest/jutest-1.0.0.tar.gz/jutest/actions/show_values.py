import pandas as pd

from jutest.settings import NAN_VALUE
from jutest.utils.choise import choice
from jutest.utils.display import display


def show_values(dataframe: pd.DataFrame, where: dict, **kwargs):
    for key, value in where.items():
        if value is None or value == NAN_VALUE:
            dataframe = dataframe[dataframe[key].isnull()]
        else:
            dataframe = dataframe[dataframe[key] == value]
    values = choice(dataframe, **kwargs)
    display(values, **kwargs)
