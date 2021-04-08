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

from unittest import TestCase
from unittest.mock import patch

from providah.factories.package_factory import PackageFactory as providah_pkg_factory
from tabulate import tabulate

from hdc.core.catalog.crawler import Crawler
from hdc.core.catalog.hive_crawler import HiveCrawler
from hdc.core.dao.dao import DAO
from hdc.core.dao.jdbc_connector import JdbcConnector
from hdc.core.dao.rdbms_dao import RdbmsDAO


class TestHiveCrawler(TestCase):
    print_sample = False

    def setUp(self) -> None:
        self._app_config = {"sources": {
            "hive": {
                "type": "HiveCrawler",
                "conf": {
                    "type": "Hive",
                    "profile": "hive_jdbc"}
            }
        }
        }
        self._profiles = {
            'hive_jdbc': {
                'protocol': 'jdbc',
                'user': '<metastore user name>',
                'password': '<metastore user password>',
                'connection_url': '<metastore jdbc connection url>',
                'database': '<hive database to crawl>',
                'driver': {
                    'name': 'Hive.jdbc.HiveDriver',
                    'path': '<jar path>'
                }
            }
        }

        self._sample_column_desc = [('DATABASE_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('SCHEMA_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('TABLE_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('COLUMN_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('COLUMN_TYPE', 'VARCHAR', 100, 100, 0, 0, True,)]

        self._sample_query_result = [('HR', 'FINANCE', 'ACCOUNTS_2020',
                                      'NARRATIVE', 'VARCHAR')]

        self._crawler: Crawler = providah_pkg_factory.create(key=self._app_config['sources']['hive']['type'],
                                                             library='hdc',
                                                             configuration={
                                                                 'conf': self._app_config['sources']['hive']['conf']}
                                                             )

    def test_crawler_instantiation(self):
        self.assertIsNotNone(self._crawler)
        self.assertIsInstance(self._crawler, HiveCrawler)

    @patch.object(JdbcConnector, 'connection')
    @patch.object(DAO, '_read_connection_profile')
    @patch.object(RdbmsDAO, '_test_connection')
    def test_obtain_catalog_via_jdbc(self, mock_test_connection, mock_read_connection_profile, mock_connection):
        # Setup the mock object and any expected invocations on it
        connection_profile = self._profiles['hive_jdbc']
        mock_read_connection_profile.return_value = connection_profile
        mock_test_connection.return_value = True
        connection_obj = mock_connection.return_value
        mock_cursor = connection_obj.cursor.return_value
        mock_cursor.description = self._sample_column_desc
        mock_cursor.fetchall.return_value = self._sample_query_result

        # Execute the crawler.obtain_catalog() method against it
        df_catalog = self._crawler.obtain_catalog()

        # Make assertions
        mock_connection.assert_called_with({
            "jclassname": connection_profile['driver']['name'],
            "jars": connection_profile['driver']['path'],
            "url": connection_profile['connection_url'],
            "user": connection_profile['user'],
            "password": connection_profile['password']
        })
        self.assertIsNotNone(df_catalog)
        self.assertFalse(df_catalog.empty)

        if TestHiveCrawler.print_sample:
            print(f'{self.__str__()}:\n{tabulate(df_catalog, headers="keys", tablefmt="pretty", showindex=False)}')
