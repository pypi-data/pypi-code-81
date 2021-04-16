# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from pathlib import Path
import logging
from configparser import ConfigParser
from typing import Dict, List
import sqlite3

from threedi_settings.mappings import get_sqlite_table_schemas, SettingsTables

logger = logging.getLogger(__name__)


class ThreedimodelIni:
    """
    Interface to the 3Di model ini file through the `config` attribute, a
    `ConfigParser` instance. You can also parse the data into a dictionary
    using the as_dict() method.
    """

    def __init__(self, config_file: Path):
        """
        :param config_file: configuration ini file
        """
        self.config_file = config_file
        assert (
            self.config_file.exists() and not self.config_file.is_dir()
        ), f"{self.config_file} does not exist or is a dir"

        self.config = ConfigParser()
        with open(self.config_file, "r") as ini_file:
            self.config.read_file(ini_file)

    def as_dict(self, flat: bool = True) -> Dict:
        """
        Parse the file into a dictionary.

        To keep the sections defined in the ini file, call with `flat=False`
        """
        d = {}
        sections = self.config.sections()

        for section in sections:
            options = self.config.options(section)
            temp_dict = {}
            for option in options:
                if not flat:
                    temp_dict[option] = self.config.get(section, option)
                    d[section] = temp_dict
                    continue
                d[option] = self.config.get(section, option)
        return d


class AggregationIni:
    """
    Interface to the 3Di model aggregation file through the `aggregation`
    attribute, a `ConfigParser` instance. You can also parse the data
    into a dictionary using the as_dict() method.
    """

    def __init__(self, aggregation_file: Path):
        self.aggregation = ConfigParser()
        self.aggregation_ini = aggregation_file
        with open(self.aggregation_ini, "r") as aggr_file:
            self.aggregation.read_file(aggr_file)

    def as_dict(self) -> Dict:
        sections_dict = {}

        # get sections and iterate over each
        sections = self.aggregation.sections()

        for section in sections:
            options = self.aggregation.options(section)
            temp_dict = {}
            for option in options:
                temp_dict[option] = self.aggregation.get(section, option)

            sections_dict[section] = temp_dict

        return sections_dict


class ThreedimodelSqliteBase:
    def __init__(self, sqlite_file: Path):
        self.sqlite_file = sqlite_file
        assert sqlite_file.exists() and sqlite_file.is_file(), f"file {sqlite_file} does not exist"
        self.setup_db()

    def setup_db(self):
        conn = sqlite3.connect(self.sqlite_file)
        conn.row_factory = sqlite3.Row
        self.cursor = conn.cursor()


class RowDoesNotExistError(Exception):
    pass


class ThreedimodelSqlite(ThreedimodelSqliteBase):
    """
    Interface to the 3Di model sqlite file
    """

    def __init__(self, sqlite_file: Path, row_id: int):
        super().__init__(sqlite_file=sqlite_file)
        self.row_id = row_id
        self.table_schemas = get_sqlite_table_schemas()
        self._global_settings = None
        self._numerical_settings = None
        self._aggregation_settings = None

    @property
    def global_settings(self) -> Dict:
        """
        :raises RowDoesNotExistError if the given table row does not exist
        """

        if not self._global_settings:
            self._global_settings = self._get_global_settings()
        return self._global_settings

    @property
    def numerical_settings(self) -> Dict:
        """
        :raises RowDoesNotExistError if the given table row does not exist
        """
        if not self._numerical_settings:
            self._numerical_settings = self._get_numerical_settings()
        return self._numerical_settings

    @property
    def aggregation_settings(self) -> Dict:
        if not self._aggregation_settings:
            self._aggregation_settings = self._get_aggregation_settings()
        return self._aggregation_settings

    def get_global_settings_ids(self) -> Dict:
        statement = f"SELECT id, name FROM {SettingsTables.global_settings.value}"
        self.cursor.execute(statement)
        return dict(self.cursor.fetchall())
        # d = dict()
        # for entry in self.cursor.fetchall():
        #     d[i] = dict(entry)
        # return d
        # return [x["id"] for x in self.cursor.fetchall()]

    def _get_global_settings(self) -> Dict:
        """
        :raises RowDoesNotExistError if the given table row does not exist
        """
        field_names = self.table_schemas[SettingsTables.global_settings]
        fn = ",".join(field_names)
        fn += ",numerical_settings_id"
        statement = f"SELECT {fn} FROM {SettingsTables.global_settings.value} WHERE id={self.row_id}"
        self.cursor.execute(statement)
        try:
            return dict(self.cursor.fetchone())
        except TypeError:
            raise RowDoesNotExistError(
                f"v2_global_settings row with ID {self.row_id} does not exist"
            )

    def _get_numerical_settings(self) -> Dict:
        """
        :raises RowDoesNotExistError if the given table row does not exist
        """
        field_names = self.table_schemas[SettingsTables.numerical_settings]
        fn = ",".join(field_names)
        row_id = self.global_settings["numerical_settings_id"]
        statement = f"SELECT {fn} FROM {SettingsTables.numerical_settings.value} WHERE id={row_id}"
        self.cursor.execute(statement)
        return dict(self.cursor.fetchone())

    def _get_aggregation_settings(self) -> Dict:
        field_names = self.table_schemas[SettingsTables.aggregation_settings]
        fn = ",".join(field_names)
        statement = f"SELECT {fn} FROM {SettingsTables.aggregation_settings.value}"
        self.cursor.execute(statement)
        d = dict()
        for i, entry in enumerate(self.cursor.fetchall()):
            d[i] = dict(entry)
        return d

    def as_dict(self) -> Dict:
        """
        :raises RowDoesNotExistError if the given table row does not exist
        """
        return {
            **self.global_settings,
            **self.numerical_settings
        }
