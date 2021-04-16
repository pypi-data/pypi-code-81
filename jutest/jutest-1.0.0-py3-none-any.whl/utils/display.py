import pandas as pd
from IPython.core.display import HTML, display as jupyter_display

from jutest.utils.format_dataframe import FormatDataFrame

MAX_ROWS_OPTION_NAME = 'max_rows'
MAX_COLWIDTH_OPTION_NAME = 'display.max_colwidth'


def display(data, html: bool = False, full_width: bool = False, **kwargs):
    if html:
        data = _to_html(data)
    pd.set_option(MAX_ROWS_OPTION_NAME, None)
    if full_width:
        pd.set_option(MAX_COLWIDTH_OPTION_NAME, 0)
    if isinstance(data, pd.DataFrame):
        format_dataframe = FormatDataFrame(data)
        data = format_dataframe.format(full_width=full_width, **kwargs)
    jupyter_display(data)
    pd.reset_option(MAX_ROWS_OPTION_NAME)
    pd.reset_option(MAX_COLWIDTH_OPTION_NAME)


def warning(text: str):
    display(f'<b>Warning:</b> {text}', html=True)


def _to_html(text: str):
    return HTML(text)
