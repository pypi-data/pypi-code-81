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
from hdc.core.catalog.oracle_crawler import OracleCrawler
from hdc.core.dao.dao import DAO
from hdc.core.dao.jdbc_connector import JdbcConnector
from hdc.core.dao.odbc_connector import OdbcConnector
from hdc.core.dao.oracle import Oracle


class TestOracleCrawler(TestCase):
    print_sample = False

    def setUp(self) -> None:
        self._app_config = {"sources": {
            "oracle": {
                "type": "OracleCrawler",
                "conf": {
                    "type": "Oracle",
                    "profile": "oracle_local_profile"}
            }
        }
        }
        self._profiles = {
            'oracle_jdbc': {
                'protocol': 'jdbc',
                'host': 'localhost',
                'port': 1521,
                'sid': 'XEPDB1',
                'user': 'hdc_user',
                'password': 'hdc12345',
                'driver': {
                    'name': 'oracle.jdbc.OracleDriver',
                    'path': '<jar path>'
                }
            },
            "oracle_odbc":
                {
                    "protocol": "odbc",
                    "host": "<host>",
                    "port": "<port>",
                    "database": "<database_name>",
                    "user": "<user_name>",
                    "password": "<password>",
                    "driver":
                        {"name": "<ODBC Driver Name>"}
                },
            "oracle_cx":
                {"protocol": "cx_oracle",
                 "host": "< host >",
                 "port": "< port >",
                 "sid": "< Oracle instance identifier >",
                 "user": "< user_name >",
                 "password": "< password >",
                 "client_library_dir": "< client_library_dir >"}
        }

        self._sample_column_desc = [('DATABASE_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('SCHEMA_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('TABLE_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('COLUMN_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('COLUMN_TYPE', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('COLUMN_SIZE', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('IS_NULL', 'VARCHAR', 100, 100, 0, 0, True,)]

        self._sample_query_result = [('HR', 'FINANCE', 'ACCOUNTS_2020',
                                      'NARRATIVE', 'VARCHAR', 1000,
                                      'NOT NULL')]

        self._crawler: Crawler = providah_pkg_factory.create(key=self._app_config['sources']['oracle']['type'],
                                                             library='hdc',
                                                             configuration={
                                                                 'conf': self._app_config['sources']['oracle']['conf']}
                                                             )

    def test_crawler_instantiation(self):
        self.assertIsNotNone(self._crawler)
        self.assertIsInstance(self._crawler, OracleCrawler)

    @patch.object(JdbcConnector, 'connection')
    @patch.object(DAO, '_read_connection_profile')
    @patch.object(Oracle, '_test_connection')
    def test_obtain_catalog_via_jdbc(self, mock_test_connection, mock_read_connection_profile, mock_connection):
        # Setup the mock object and any expected invocations on it
        connection_profile = self._profiles['oracle_jdbc']
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
            "url": f"jdbc:oracle:thin:@{connection_profile['host']}:{connection_profile['port']}:{connection_profile['sid']}",
            "user": connection_profile['user'],
            "password": connection_profile['password']
        })
        self.assertIsNotNone(df_catalog)
        self.assertFalse(df_catalog.empty)

        if TestOracleCrawler.print_sample:
            print(f'{self.__str__()}:\n{tabulate(df_catalog, headers="keys", tablefmt="pretty", showindex=False)}')

    @patch.object(OdbcConnector, 'connection')
    @patch.object(DAO, '_read_connection_profile')
    @patch.object(Oracle, '_test_connection')
    def test_obtain_catalog_via_odbc(self, mock_test_connection, mock_read_connection_profile, mock_connection):
        # Setup the mock object and any expected invocations on it
        connection_profile = self._profiles['oracle_odbc']
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
            "driver": connection_profile['driver']['name'],
            "connection_string": f"DRIVER={connection_profile['driver']['name']};SERVER={connection_profile['host']};"
                                 f"PORT={connection_profile['port']};DATABASE={connection_profile['database']};"
                                 f"UID={connection_profile['user']};PWD={connection_profile['password']};"
        })
        self.assertIsNotNone(df_catalog)
        self.assertFalse(df_catalog.empty)

        if TestOracleCrawler.print_sample:
            print(f'{self.__str__()}:\n{tabulate(df_catalog, headers="keys", tablefmt="pretty", showindex=False)}')

    @patch('hdc.core.dao.oracle.cx_Oracle', autospec=True)
    @patch.object(DAO, '_read_connection_profile')
    @patch.object(Oracle, '_test_connection')
    def test_obtain_catalog_via_cx_oracle(self, mock_test_connection, mock_read_connection_profile, mock_cx_oracle):
        # Setup the mock object and any expected invocations on it
        connection_profile = self._profiles['oracle_cx']
        mock_read_connection_profile.return_value = connection_profile
        mock_test_connection.return_value = True
        mock_cx_oracle.makedsn.return_value = ()
        connection_obj = mock_cx_oracle.connect.return_value
        mock_cursor = connection_obj.cursor.return_value
        mock_cursor.description = self._sample_column_desc
        mock_cursor.fetchall.return_value = self._sample_query_result

        # Execute the crawler.obtain_catalog() method against it
        df_catalog = self._crawler.obtain_catalog()

        # Make assertions
        mock_cx_oracle.makedsn.assert_called_with(connection_profile['host'], connection_profile['port'],
                                                  connection_profile['sid'])
        mock_cx_oracle.connect.assert_called_with(connection_profile['user'], connection_profile['password'], dsn=())
        self.assertIsNotNone(df_catalog)
        self.assertFalse(df_catalog.empty)

        if TestOracleCrawler.print_sample:
            print(f'{self.__str__()}:\n{tabulate(df_catalog, headers="keys", tablefmt="pretty", showindex=False)}')
