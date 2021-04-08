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

import pandas as pd

from hdc.core.map.mapper import Mapper


class HdfsToSnowflake(Mapper):
    avro_to_snowflake_data_type_map = {
        "BOOLEAN": "BOOLEAN",
        "INT": "INTEGER",
        "LONG": "INTEGER",
        "FLOAT": "FLOAT",
        "DOUBLE": "DOUBLE",
        "STRING": "VARCHAR",
        "BYTES": "BINARY"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def map_assets(self, df_catalog) -> list:

        # Default database for all HDFS data assets
        df_catalog['DATABASE_NAME'] = 'HDFS'
        sql_ddl_list = self.__map_databases(["HDFS"])

        # Default schema for all HDFS data assets
        df_catalog['SCHEMA_NAME'] = 'DEFAULT'
        sql_ddl_list.extend(self.__map_schemas("HDFS", ["DEFAULT"]))

        # Extract the first common ancestor (directory)
        df_catalog['TABLE_NAME'] = df_catalog['PARENT'].map(self.__get_path_name)
        df_catalog = df_catalog[['DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME']].drop_duplicates()

        # DDL for all tables under each unique database and schema
        sql, df_catalog_report = self.__map_tables(df_catalog)
        sql_ddl_list.extend(sql)

        if self._conf.get("report", False):
            self._build_report(df_catalog_report)

        return sql_ddl_list

    def __map_databases(self, databases) -> list:
        return [f'CREATE DATABASE IF NOT EXISTS "{db.upper()}"' for db in databases]

    def __map_schemas(self, database, schemas) -> list:
        return [f'CREATE SCHEMA IF NOT EXISTS "{database.upper()}"."{schema.upper()}"' for schema in schemas]

    def __map_data_types(self, df_catalog) -> pd.DataFrame:
        distinct_tables = df_catalog['TABLE_NAME'].unique()
        dd = {
            'TABLE_NAME': [],
            'COLUMN_NAME': [],
            'COLUMN_TYPE': [],
            'TARGET_COLUMN_TYPE': []
        }
        for table in distinct_tables:
            try:
                table_schema = self._conf['schema'][table]
                dd['TABLE_NAME'].extend([table for _ in table_schema['fields']])
                dd['COLUMN_NAME'].extend([field['name'] for field in table_schema['fields']])
                dd['COLUMN_TYPE'].extend([field['type'] for field in table_schema['fields']])
                mapped_types = [HdfsToSnowflake.avro_to_snowflake_data_type_map.get(field['type'].upper(), '-') for
                                field in table_schema['fields']]
                dd['TARGET_COLUMN_TYPE'].extend(mapped_types)
            except KeyError:
                self.__logger.error(f"Either no schema configured for table '{table}' or configuration is incorrect")

        return pd.DataFrame(dd)

    def __map_tables(self, df_catalog: pd.DataFrame) -> tuple:
        sql_ddl = []

        # Map the first common ancestor as a table and look-up its schema from the mapper conf
        df_catalog_mapped_types = self.__map_data_types(df_catalog)
        df_merged = df_catalog.join(df_catalog_mapped_types.set_index('TABLE_NAME'), on='TABLE_NAME').reset_index()

        df_merged['COLUMN_DESC'] = df_merged['COLUMN_NAME'] + ' ' + df_merged['TARGET_COLUMN_TYPE']

        df_table_group = df_merged[
            ['DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME', 'TARGET_COLUMN_TYPE', 'COLUMN_DESC']].groupby(
            ['DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME'])

        for name, group_df in df_table_group:
            sql_ddl.append(f"CREATE OR REPLACE TABLE {'.'.join(name).upper()} "
                           f"("
                           f"{', '.join(list(group_df[~group_df['TARGET_COLUMN_TYPE'].str.contains('-')]['COLUMN_DESC'])).upper()}"
                           f", CK_SUM VARCHAR"
                           f")")

        return (sql_ddl, df_merged)

    @staticmethod
    def __get_path_name(file_path):
        from pathlib import Path
        return Path(file_path).name
