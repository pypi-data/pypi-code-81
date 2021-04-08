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

from hdc.core.map.hdfs_to_snowflake import HdfsToSnowflake
from hdc.core.map.mapper import Mapper


class TestHdfsToSnowflake(TestCase):
    print_sample = False

    def setUp(self) -> None:
        self._app_config = {
            "mappers": {
                "hdfs":
                    {"snowflake": {
                        "type": "HdfsToSnowflake",
                        "conf": {
                            "report": False,
                            "schema": {
                                "department": {"type": "record", "name": "department",
                                               "fields": [{"name": "column1", "type": "string"},
                                                          {"name": "column2", "type": "enum"}]},
                                "resources": {"type": "record", "name": "resources",
                                              "fields": [{"name": "column1", "type": "string"},
                                                         {"name": "column2", "type": "string"},
                                                         {"name": "column3", "type": "string"}]}
                            }
                        }
                    }
                    }
            }
        }

        self._mapper: Mapper = providah_pkg_factory.create(key=self._app_config['mappers']['hdfs']['snowflake']['type'],
                                                           library='hdc',
                                                           configuration={'conf': (self._app_config['mappers']['hdfs']
                                                           ['snowflake']).get('conf', {"report": False})
                                                                          }
                                                           )

    def test_mapper_instantiation(self):
        self.assertIsNotNone(self._mapper)
        self.assertIsInstance(self._mapper, HdfsToSnowflake)

    def test_map_assets(self):
        # Set expectations
        data_dict = [
            {"PARENT": "/home/dummy/resources", "FILE ASSET": "file1.csv"},
            {"PARENT": "/home/dummy/resources", "FILE ASSET": "file2.csv"},
            {"PARENT": "/home/dummy/resources/department", "FILE ASSET": "department.csv"}
        ]

        resources_table_schema = self._mapper._conf['schema']['resources']
        dept_table_schema = self._mapper._conf['schema']['department']
        catalog_dataframe = DataFrame(data_dict, columns=['PARENT', 'FILE ASSET'])

        expected_sql_ddl = [
            'CREATE DATABASE IF NOT EXISTS "HDFS"',
            'CREATE SCHEMA IF NOT EXISTS "HDFS"."DEFAULT"',
            f"CREATE OR REPLACE TABLE HDFS.DEFAULT.DEPARTMENT ("
            f"{', '.join(['COLUMN1 VARCHAR'])}"
            f", CK_SUM VARCHAR"
            f")",
            f"CREATE OR REPLACE TABLE HDFS.DEFAULT.RESOURCES ("
            f"{', '.join(['COLUMN1 VARCHAR', 'COLUMN2 VARCHAR', 'COLUMN3 VARCHAR'])}"
            f", CK_SUM VARCHAR"
            f")"
        ]

        # Execute the method to test
        sql_ddl_list = self._mapper.map_assets(catalog_dataframe)

        # Make assertions
        self.assertIsNotNone(sql_ddl_list)
        self.assertListEqual(sql_ddl_list, expected_sql_ddl)

        if TestHdfsToSnowflake.print_sample:
            from pprint import pprint
            pprint(sql_ddl_list)
