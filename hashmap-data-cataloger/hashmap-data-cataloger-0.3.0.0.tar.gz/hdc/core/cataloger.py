#  Copyright © 2020 Hashmap, Inc
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
#TODO: Module description
"""
import logging

from pandas import DataFrame
from providah.factories.package_factory import PackageFactory as providah_pkg_factory
from tabulate import tabulate

from hdc.core.catalog.crawler import Crawler
from hdc.core.exceptions.hdc_error import HdcError
from hdc.utils import file_utils


class Cataloger:
    def __init__(self, **kwargs):
        self._logger = self._get_logger()

        source = kwargs.get('source')
        app_config = file_utils.get_app_config(kwargs.get('app_config', None))

        if source in app_config['sources'].keys():
            self._crawler: Crawler = providah_pkg_factory.create(key=app_config['sources'][source]['type'],
                                                                 library='hdc',
                                                                 configuration={
                                                                     'conf': app_config['sources'][source]['conf']}
                                                                 )
        else:
            raise HdcError(message=f"{source} not registered in 'sources' in {kwargs.get('app_config') or 'hdc.yml'}")

    def _get_logger(self):
        return logging.getLogger(self.__class__.__name__)

    @staticmethod
    def pretty_print(catalog_dataframe):
        print(tabulate(catalog_dataframe, headers='keys', tablefmt="pretty", showindex=False))

    def obtain_catalog(self) -> DataFrame:
        df_catalog = None

        try:
            df_catalog = self._crawler.obtain_catalog()
        except Exception:
            import traceback as tb
            self._logger.error(f"{tb.format_exc()}")
            raise HdcError(message=f"Could not catalog the source", traceback=tb.format_exc())

        return df_catalog
