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
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from providah.factories.package_factory import PackageFactory as providah_pkg_factory
from tabulate import tabulate

from hdc.core.catalog.crawler import Crawler
from hdc.core.catalog.hdfs_crawler import HdfsCrawler
from hdc.core.dao.dao import DAO
from hdc.core.dao.hdfs import Hdfs


class TestHdfsCrawler(TestCase):
    print_sample = False

    def setUp(self) -> None:
        self._app_config = {
            "sources": {
                "hdfs": {
                    "type": "HdfsCrawler",
                    "conf": {
                        "type": "Hdfs",
                        "profile": "hdfs_dummy_profile",
                        "dir": Path.home() / "Documents" / "Work",
                        "file_format": "csv",
                        "partition_depth": 0
                    }
                }
            }
        }

        self._profiles = {
            'hdfs_dummy_profile': {
                'protocol': 'hadoop',
                'user': '<hdfs user>',
            }
        }

        self._crawler: Crawler = providah_pkg_factory.create(key=self._app_config['sources']['hdfs']['type'],
                                                             library='hdc',
                                                             configuration={
                                                                 'conf': self._app_config['sources']['hdfs']['conf']}
                                                             )

    def test_crawler_instantiation(self):
        self.assertIsNotNone(self._crawler)
        self.assertIsInstance(self._crawler, HdfsCrawler)

    @patch.object(Hdfs, 'get_directory_listing')
    @patch.object(DAO, '_read_connection_profile')
    def test_obtain_catalog(self, mock_read_connection_profile, mock_get_directory_listing):
        # Configure mock objects
        connection_profile = self._profiles['hdfs_dummy_profile']
        mock_read_connection_profile.return_value = connection_profile
        mock_get_directory_listing.side_effect = self.__for_local_test_only

        # Execute the crawler.obtain_catalog() method against it
        df_catalog = self._crawler.obtain_catalog()

        # Make assertions
        mock_get_directory_listing.assert_called_with(self._app_config['sources']['hdfs']
                                                      ['conf']['dir'],
                                                      self._app_config['sources']['hdfs']
                                                      ['conf']['file_format'])
        self.assertIsNotNone(df_catalog)
        self.assertFalse(df_catalog.empty)

        if TestHdfsCrawler.print_sample:
            print(f'{self.__str__()}:\n{tabulate(df_catalog, headers="keys", tablefmt="pretty", showindex=False)}')

    @staticmethod
    def __for_local_test_only(dir_path, format):
        import subprocess as sp
        local_proc1 = sp.run(f'find {dir_path} -name "*.{format}"', stdout=sp.PIPE, shell=True)
        dir_listing = local_proc1.stdout.decode().strip().split('\n')
        return dir_listing
