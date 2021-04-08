# Copyright © 2020 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase
from unittest.mock import patch

from providah.factories.package_factory import PackageFactory as providah_pkg_factory
from tabulate import tabulate

from hdc.core.catalog.crawler import Crawler
from hdc.core.catalog.netezza_crawler import NetezzaCrawler
from hdc.core.dao.dao import DAO
from hdc.core.dao.jdbc_connector import JdbcConnector
from hdc.core.dao.odbc_connector import OdbcConnector
from hdc.core.dao.rdbms_dao import RdbmsDAO


class TestNetezzaCrawler(TestCase):
    print_sample = False

    def setUp(self) -> None:
        self._app_config = {"sources": {
            "netezza": {
                "type": "NetezzaCrawler",
                "conf": {
                    "type": "Netezza",
                    "profile": "netezza_jdbc"}
            }
        }
        }
        self._profiles = {
            'netezza_jdbc': {
                'protocol': 'jdbc',
                'host': '<host>',
                'port': '<port>',
                'database': '<database>',
                'user': 'hdc_user',
                'password': 'hdc12345',
                'driver': {
                    'name': '<java class name>',
                    'path': '<jar path>'
                }
            },
            "netezza_odbc":
                {
                    "protocol": "odbc",
                    "host": "<host>",
                    "port": "<port>",
                    "database": "<database_name>",
                    "user": "<user_name>",
                    "password": "<password>",
                    "driver":
                        {"name": "<ODBC Driver Name>"}
                }
        }

        self._sample_column_desc = [('DATABASE', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('SCHEMA_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('TABLE_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('COLUMN_NAME', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('COLUMN_TYPE', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('COLUMN_SIZE', 'VARCHAR', 100, 100, 0, 0, True,),
                                    ('IS_NULL', 'VARCHAR', 100, 100, 0, 0, True,)]

        self._sample_query_result = [('HR', 'FINANCE', 'ACCOUNTS_2020',
                                      'NARRATIVE', 'VARCHAR', 1000,
                                      'NOT NULL')]

        self._crawler: Crawler = providah_pkg_factory.create(key=self._app_config['sources']['netezza']['type'],
                                                             library='hdc',
                                                             configuration={
                                                                 'conf': self._app_config['sources']['netezza']['conf']}
                                                             )

    def test_crawler_instantiation(self):
        self.assertIsNotNone(self._crawler)
        self.assertIsInstance(self._crawler, NetezzaCrawler)

    @patch.object(JdbcConnector, 'connection')
    @patch.object(DAO, '_read_connection_profile')
    @patch.object(RdbmsDAO, '_test_connection')
    def test_obtain_catalog_via_jdbc(self, mock_test_connection, mock_read_connection_profile, mock_connection):
        # Setup the mock object and any expected invocations on it
        connection_profile = self._profiles['netezza_jdbc']
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
            "url": f"jdbc:netezza://{connection_profile['host']}:{connection_profile['port']}/{connection_profile['database']}",
            "user": connection_profile['user'],
            "password": connection_profile['password']
        })
        self.assertIsNotNone(df_catalog)
        self.assertFalse(df_catalog.empty)

        if TestNetezzaCrawler.print_sample:
            print(f'{self.__str__()}:\n{tabulate(df_catalog, headers="keys", tablefmt="pretty", showindex=False)}')

    @patch.object(OdbcConnector, 'connection')
    @patch.object(DAO, '_read_connection_profile')
    @patch.object(RdbmsDAO, '_test_connection')
    def test_obtain_catalog_via_odbc(self, mock_test_connection, mock_read_connection_profile, mock_connection):
        # Setup the mock object and any expected invocations on it
        connection_profile = self._profiles['netezza_odbc']
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

        if TestNetezzaCrawler.print_sample:
            print(f'{self.__str__()}:\n{tabulate(df_catalog, headers="keys", tablefmt="pretty", showindex=False)}')

    # def test_get_database_names(self):
    # mock_db_result = [('TEST',)]
    # expected_response = ['TEST']
    #
    # execute = self._mock.cursor.return_value
    # execute.fetchall.return_value = mock_db_result
    #
    # self.assertEqual(NetezzaCrawler._get_database_names(self._mock), expected_response)

    # def test_get_schema_names_by_db(self):
    # mock_db_result = [('ADMIN',), ('DEFINITION_SCHEMA',), ('INFORMATION_SCHEMA',)]
    # expected_response = ['ADMIN', 'DEFINITION_SCHEMA', 'INFORMATION_SCHEMA']
    #
    # execute = self._mock.cursor.return_value
    # execute.fetchall.return_value = mock_db_result
    #
    # self.assertEqual(NetezzaCrawler._get_schema_names_by_db('TEST', self._mock), expected_response)

    # def test_get_tables_by_db(self):
    # mock_db_result = [('TEST', 'ADMIN', 'ABC', 'T1', 'INTEGER', 4, False, None),
    #                   ('TEST', 'ADMIN', 'ABC', 'T5', 'CHARACTER VARYING(400)', -1, False, None),
    #                   ('TEST', 'ADMIN', 'ABC', 'C_SUM', 'CHARACTER VARYING(64000)', -1, False, None),
    #                   ('TEST', 'ADMIN', 'TEST1', 'T1', 'INTEGER', 4, False, None),
    #                   ('TEST', 'ADMIN', 'TEST1', 'T5', 'CHARACTER VARYING(400)', -1, False, None),
    #                   ('TEST', 'ADMIN', 'TEST2', 'U1', 'INTEGER', 4, False, None),
    #                   ('TEST', 'ADMIN', 'TEST2', 'U5', 'CHARACTER VARYING(400)', -1, False, None)]
    #
    # expected_response = {'TEST.ADMIN.ABC': [
    #     {'database': 'TEST', 'schema': 'ADMIN', 'name': 'ABC', 'columnName': 'T1', 'columnType': 'INTEGER',
    #      'columnSize': 4,
    #      'notNull': False, 'default': None},
    #     {'database': 'TEST', 'schema': 'ADMIN', 'name': 'ABC', 'columnName': 'T5',
    #      'columnType': 'CHARACTER VARYING(400)', 'columnSize': -1, 'notNull': False, 'default': None},
    #     {'database': 'TEST', 'schema': 'ADMIN', 'name': 'ABC', 'columnName': 'C_SUM',
    #      'columnType': 'CHARACTER VARYING(64000)', 'columnSize': -1, 'notNull': False, 'default': None}],
    #     'TEST.ADMIN.TEST1': [
    #         {'database': 'TEST', 'schema': 'ADMIN', 'name': 'TEST1', 'columnName': 'T1',
    #          'columnType': 'INTEGER',
    #          'columnSize': 4, 'notNull': False, 'default': None},
    #         {'database': 'TEST', 'schema': 'ADMIN', 'name': 'TEST1',
    #          'columnName': 'T5', 'columnType': 'CHARACTER VARYING(400)',
    #          'columnSize': -1, 'notNull': False, 'default': None}],
    #     'TEST.ADMIN.TEST2': [
    #         {'database': 'TEST', 'schema': 'ADMIN', 'name': 'TEST2', 'columnName': 'U1',
    #          'columnType': 'INTEGER',
    #          'columnSize': 4, 'notNull': False, 'default': None},
    #         {'database': 'TEST', 'schema': 'ADMIN', 'name': 'TEST2',
    #          'columnName': 'U5', 'columnType': 'CHARACTER VARYING(400)',
    #          'columnSize': -1, 'notNull': False, 'default': None}]}
    #
    # execute = self._mock.cursor.return_value
    # execute.fetchall.return_value = mock_db_result
    #
    # self.assertEqual(NetezzaCrawler._get_tables_by_db('TEST', self._mock), expected_response)
