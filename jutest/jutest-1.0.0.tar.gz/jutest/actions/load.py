import pandas as pd

from jutest.utils.choise import choice
from jutest.utils.display import display


def load(filename: str, show: bool = True, choicer='preview', **kwargs):
    dataframe = pd.read_csv(filename)
    if show:
        preview = choice(dataframe, choicer=choicer, **kwargs)
        display(preview, **kwargs)
    return dataframe
