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

from providah.factories.package_factory import PackageFactory as providah_pkg_factory

from hdc.core.catalog.crawler import Crawler
from hdc.core.create.creator import Creator
from hdc.core.exceptions.hdc_error import HdcError
from hdc.core.map.mapper import Mapper
from hdc.utils import file_utils


class AssetMapper:

    def __init__(self, **kwargs):
        self._logger = self._get_logger()
        source = kwargs.get('source')
        destination = kwargs.get('destination')
        app_config = file_utils.get_app_config(kwargs.get('app_config', None))

        if source in app_config['sources'].keys():
            self._crawler: Crawler = providah_pkg_factory.create(key=app_config['sources'][source]['type'],
                                                                 library='hdc',
                                                                 configuration={'conf': app_config['sources'][source][
                                                                     'conf']})
        else:
            raise HdcError(message=f"{source} not registered in 'sources' in {kwargs.get('app_config') or 'hdc.yml'}")

        if source in app_config['mappers'].keys() and destination in app_config['mappers'][source].keys():
            self._mapper: Mapper = providah_pkg_factory.create(key=app_config['mappers'][source][destination]['type'],
                                                               library='hdc',
                                                               configuration={'conf': (app_config['mappers']
                                                               [source]
                                                               [destination]
                                                               ).get('conf', {"report": False})})
        else:
            raise HdcError(
                message=f"{source}/{destination} not registered in 'mappers' in {kwargs.get('app_config') or 'hdc.yml'}")


        if destination in app_config['destinations'].keys():
            self._creator: Creator = providah_pkg_factory.create(key=app_config['destinations'][destination]['type'],
                                                                 library='hdc',
                                                                 configuration={'conf': app_config['destinations'][
                                                                     destination]['conf']})
        else:
            raise HdcError(
                message=f"{destination} not registered in 'destinations' in {kwargs.get('app_config') or 'hdc.yml'}")

    def map_assets(self) -> bool:
        success = False
        try:
            catalog_dataframe = self._crawler.obtain_catalog()
            if catalog_dataframe is not None:
                sql_ddl_list = self._mapper.map_assets(catalog_dataframe)
                self._logger.debug(sql_ddl_list)
                self._creator.replicate_structures(sql_ddl_list)
                success = True
        except Exception:
            import traceback as tb
            self._logger.error(f"{tb.format_exc()}")
            raise HdcError(message=f"Failed to map the source to destination", traceback=tb.format_exc())

        return success

    def _get_logger(self):
        return logging.getLogger(self.__class__.__name__)
