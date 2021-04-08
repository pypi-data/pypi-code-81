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

import pandas as pd

from hdc.core.map.mapper import Mapper


class OracleToSnowflake(Mapper):
    data_type_map = {
        "VARCHAR": "(.?(VARCHAR).?)|(.?(CHAR).?)",
        "DATE": "DATE",
        "TIME": "TIMESTAMP",
        "NUMERIC": "NUMBER",
        "REAL": "FLOAT",
        "BINARY": "BINARY_FLOAT|BINARY_DOUBLE"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def map_assets(self, df_catalog: pd.DataFrame) -> list:
        unique_databases = df_catalog['DATABASE_NAME'].unique()

        # DDL for all unique databases
        sql_ddl_list = self.__map_databases(unique_databases)

        # DDL for all schemas under each unique database
        for db in unique_databases:
            db_filter = df_catalog['DATABASE_NAME'] == db
            sql_ddl_list.extend(self.__map_schemas(db, df_catalog[db_filter]['SCHEMA_NAME'].unique()))

        # DDL for all tables under each unique database and schema
        sql_ddl_list.extend(self.__map_tables(df_catalog))

        if self._conf.get("report", False):
            self._build_report(df_catalog)

        return sql_ddl_list

    @staticmethod
    def __map_databases(databases) -> list:
        return [f'CREATE DATABASE IF NOT EXISTS "{db.upper()}"' for db in databases]

    @staticmethod
    def __map_schemas(database, schemas) -> list:
        return [f'CREATE SCHEMA IF NOT EXISTS "{database.upper()}"."{schema.upper()}"' for schema in schemas]

    @staticmethod
    def __map_data_types(src_data_type: pd.Series) -> pd.Series:
        keep = "|".join(OracleToSnowflake.data_type_map.values())
        discard = f"(?!{keep})"
        supported_data_types = src_data_type.str.match(keep)
        unsupported_data_types = src_data_type.str.match(discard)
        target_data_type = src_data_type[supported_data_types]
        for target_type, source_type in OracleToSnowflake.data_type_map.items():
            target_data_type = target_data_type.str.replace(source_type, target_type, case=False)

        return pd.concat([
            target_data_type,
            src_data_type[unsupported_data_types].str.replace('.*', '-', regex=True)
        ])

    @staticmethod
    def __map_null_clause(src_null_clause: pd.Series) -> pd.Series:
        return src_null_clause.map(lambda not_null: "NOT NULL" if not_null == 'N' else "")

    def __map_tables(self, df_catalog: pd.DataFrame) -> list:
        sql_ddl = []

        df_catalog['TARGET_COLUMN_TYPE'] = self.__map_data_types(df_catalog['COLUMN_TYPE'])
        df_catalog['TARGET_NOT_NULL'] = self.__map_null_clause(df_catalog['NOT_NULL'])
        df_catalog['COLUMN_DESC'] = df_catalog['COLUMN_NAME'] \
                                    + ' ' \
                                    + df_catalog['TARGET_COLUMN_TYPE'] \
                                    + ' ' \
                                    + df_catalog['TARGET_NOT_NULL']

        df_table_group = df_catalog[
            ['DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME', 'TARGET_COLUMN_TYPE', 'COLUMN_DESC']].groupby(
            ['DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME'])

        for name, group in df_table_group:
            sql_ddl.append(f"CREATE OR REPLACE TABLE {'.'.join(name).upper()} "
                           f"("
                           f"{','.join(list(group[~group['TARGET_COLUMN_TYPE'].str.contains('-')]['COLUMN_DESC'])).upper()}"
                           f", CK_SUM VARCHAR"
                           f")")

        return sql_ddl
