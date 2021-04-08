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

from pandas import DataFrame
from providah.factories.package_factory import PackageFactory as providah_pkg_factory

from hdc.core.map.mapper import Mapper
from hdc.core.map.oracle_to_snowflake import OracleToSnowflake


class TestOracleToSnowflake(TestCase):
    print_sample = False

    def setUp(self) -> None:
        self._app_config = {
            "mappers": {
                "oracle":
                    {"snowflake": {
                        "type": "OracleToSnowflake",
                        "conf": {"report": False}
                    }}
            }
        }

        self._mapper: Mapper = providah_pkg_factory.create(
            key=self._app_config['mappers']['oracle']['snowflake']['type'],
            library='hdc',
            configuration={'conf': (self._app_config['mappers']['oracle']
            ['snowflake']).get('conf', {"report": False})
                           }
        )

    def test_mapper_instantiation(self):
        self.assertIsNotNone(self._mapper)
        self.assertIsInstance(self._mapper, OracleToSnowflake)

    def test_map_assets(self):
        # Set expectations
        data_dict = [
            ['DB1', 'SCHM1', 'TAB1', 'C1', 'NVARCHAR', '1000', 'N', 'ABCD'],
            ['DB1', 'SCHM1', 'TAB1', 'C1', 'BLAH', '1000', 'N', 'ABCD'],
            ['DB1', 'SCHM1', 'TAB2', 'C1', 'TIMESTAMP', None, 'Y', 'DD-MM-YYYY HH:MM:SS']
        ]

        catalog_dataframe = DataFrame(data_dict, columns=['DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME',
                                                          'COLUMN_NAME', 'COLUMN_TYPE', 'COLUMN_SIZE', 'NOT_NULL',
                                                          'COLUMN_DEFAULT'])

        expected_sql_ddl = [
            'CREATE DATABASE IF NOT EXISTS "DB1"',
            'CREATE SCHEMA IF NOT EXISTS "DB1"."SCHM1"',
            'CREATE OR REPLACE TABLE DB1.SCHM1.TAB1 (C1 VARCHAR NOT NULL, CK_SUM VARCHAR)',
            'CREATE OR REPLACE TABLE DB1.SCHM1.TAB2 (C1 TIME , CK_SUM VARCHAR)'
        ]

        # Execute the method to test
        sql_ddl_list = self._mapper.map_assets(catalog_dataframe)

        # Make assertions
        self.assertIsNotNone(sql_ddl_list)
        self.assertListEqual(sql_ddl_list, expected_sql_ddl)

        if TestOracleToSnowflake.print_sample:
            from pprint import pprint
            pprint(sql_ddl_list)
