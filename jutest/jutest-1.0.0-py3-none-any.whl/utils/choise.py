import typing

import pandas as pd

from jutest.settings import DEFAULT_CHOICER, DEFAULT_LIMIT
from jutest.utils.display import warning


def choice(dataframe: typing.Union[pd.DataFrame, pd.Series],
           choicer: str = DEFAULT_CHOICER,
           limit: int = DEFAULT_LIMIT,
           **kwargs) -> pd.DataFrame:
    length = len(dataframe)
    if choicer == 'head':
        return dataframe.head(limit)
    if choicer == 'tail':
        return dataframe.tail(limit)
    if choicer == 'preview':
        if length <= 2 * limit:
            return dataframe.copy()
        else:
            return pd.concat([
                dataframe.head(limit),
                dataframe.tail(limit)
            ])
    if choicer == 'random':
        if limit and limit > length:
            warning(f'Limit value ({limit}) must be less or equal to dataframe length ({length})')
            limit = None
        return dataframe.sample(limit)
