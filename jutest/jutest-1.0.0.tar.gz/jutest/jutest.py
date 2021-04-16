import pandas as pd

from jutest.actions.contains import ContainsAction
from jutest.actions.info import InfoAction
from jutest.actions.load import load
from jutest.actions.show_duplicates import show_duplicates
from jutest.actions.show_encodings import show_encodings
from jutest.actions.show_nulls import show_nulls
from jutest.actions.show_outliers import show_outliers
from jutest.actions.show_popularity import show_popularity
from jutest.actions.show_values import show_values
from jutest.encode.checker import EncodeChecker
from jutest.settings import DEFAULT_INFO_PRECISION


class Jutest:
    def __init__(self):
        self.dataframe = pd.DataFrame()
        self.encode_checker = EncodeChecker()

    def load(self, filename: str, show: bool = True, **kwargs):
        """
        Load CSV file
        :param filename: name of CSV file
        :param show: [optional] display result in screen
        :return:
        """
        self.dataframe = load(filename, show, **kwargs)

    def info(self, precision: int = DEFAULT_INFO_PRECISION):
        info_action = InfoAction(self.dataframe, self.encode_checker)
        info_action.info(precision)

    def show_values(self, where: dict, **kwargs):
        show_values(self.dataframe, where, **kwargs)

    def show_nulls(self, column_name: str = None, **kwargs):
        show_nulls(self.dataframe, column_name, **kwargs)

    def show_outliers(self, column_name: str, **kwargs):
        show_outliers(self.dataframe, column_name, **kwargs)

    def show_encodings(self, column_name: str, **kwargs):
        show_encodings(self.dataframe, self.encode_checker, column_name, **kwargs)

    def show_duplicates(self, column_names: list, limit_groups: int = 5, limit: int = 3, **kwargs):
        show_duplicates(self.dataframe, column_names, limit_groups, limit=limit, **kwargs)

    def show_popularity(self, column_name: str, **kwargs):
        show_popularity(self.dataframe, column_name, **kwargs)

    def contains(self, filename: str, column_name: str, **kwargs):
        contains_action = ContainsAction(filename)
        contains_action.contains(self.dataframe, column_name, **kwargs)
