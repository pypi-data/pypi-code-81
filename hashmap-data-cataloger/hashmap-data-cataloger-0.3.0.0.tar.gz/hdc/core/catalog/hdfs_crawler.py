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
from pandas import DataFrame
from providah.factories.package_factory import PackageFactory as providah_pkg_factory

from hdc.core.catalog.crawler import Crawler
from hdc.core.dao.filesystem_dao import FileSystemDAO


class HdfsCrawler(Crawler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def obtain_catalog(self) -> DataFrame:
        try:
            dao: FileSystemDAO = providah_pkg_factory.create(key=self._conf['type'].capitalize(),
                                                             library='hdc',
                                                             configuration={'connection': self._conf['profile']})

            df_filesystem_catalog = self._fetch_all(dao,
                                                    dir_path=self._conf.get("dir", "/".join(
                                                        ["/user", dao.get_conn_profile_key("user")])),
                                                    format=self._conf.get("file_format", "csv"),
                                                    partition_depth=self._conf.get("partition_depth", 0))

            return df_filesystem_catalog
        except:
            raise

        return None

    def _fetch_all(self, dao, dir_path, format, partition_depth) -> DataFrame:
        try:
            dir_listing = dao.get_directory_listing(dir_path, format)
            if dir_listing is not None:
                return DataFrame([self.__get_common_parent(file, partition_depth) for file in dir_listing])
        except:
            raise

        return None

    @staticmethod
    def __get_common_parent(file_path, partition_depth):
        from pathlib import Path
        fp = Path(file_path)
        parent = fp.parent
        for itr in range(partition_depth):
            parent = parent.parent
        return {'PARENT': str(parent), 'FILE ASSET': fp.name}
