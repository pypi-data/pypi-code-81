import pandas as pd

from jutest.utils.choise import choice
from jutest.utils.display import display


def show_popularity(dataframe: pd.DataFrame, column_name: str, full_width: bool = True, **kwargs):
    column = dataframe[column_name]
    popularity = column.value_counts()
    count = len(popularity)
    display(f'Total unique values: <b>{count}</b>', html=True)
    popularity = choice(popularity, **kwargs)
    display(popularity, full_width=full_width, **kwargs)
