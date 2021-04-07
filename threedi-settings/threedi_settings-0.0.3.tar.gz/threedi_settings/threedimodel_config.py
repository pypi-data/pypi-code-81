# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from pathlib import Path
import logging
from configparser import ConfigParser
from typing import Optional, Dict

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
