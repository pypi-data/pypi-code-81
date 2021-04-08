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

from string import Template

import pandas as pd
from providah.factories.package_factory import PackageFactory as providah_pkg_factory

from hdc.core.catalog.rdbms_crawler import RdbmsCrawler
from hdc.core.dao.rdbms_dao import RdbmsDAO


class OracleCrawler(RdbmsCrawler):
    __template_select_all_tables = Template("SELECT '$db' as DATABASE_NAME, "
                                            "'$user' as SCHEMA_NAME, "
                                            "ALL_TAB_COLUMNS.TABLE_NAME as TABLE_NAME, "
                                            "ALL_TAB_COLUMNS.COLUMN_NAME AS COLUMN_NAME, "
                                            "ALL_TAB_COLUMNS.DATA_TYPE AS COLUMN_TYPE, "
                                            "CASE "
                                            "WHEN data_precision IS NOT NULL AND NVL (data_scale, 0) > 0 "
                                            "THEN '(' || data_precision || ',' || data_scale || ')' "
                                            " WHEN data_precision IS NOT NULL AND NVL (data_scale, 0) = 0"
                                            "THEN '(' || data_precision || ')'"
                                            "END AS COLUMN_SIZE, "
                                            "ALL_TAB_COLUMNS.NULLABLE AS NOT_NULL "
                                            "FROM ALL_TAB_COLUMNS JOIN USER_TABLES "
                                            "ON (ALL_TAB_COLUMNS.TABLE_NAME = USER_TABLES.TABLE_NAME "
                                            "AND USER_TABLES.STATUS = 'VALID') ")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def obtain_catalog(self) -> pd.DataFrame:
        try:
            dao: RdbmsDAO = providah_pkg_factory.create(key=self._conf['type'].capitalize(),
                                                        library='hdc',
                                                        configuration={
                                                            'connection': self._conf['profile']})

            # Extract the table metadata/catalog from connected Oracle source
            oracle_database = dao.get_conn_profile_key("sid") if dao.get_conn_profile_key("sid") is not None \
                else dao.get_conn_profile_key("service_name")

            df_table_catalog: pd.DataFrame = self._fetch_all(dao,
                                                             query_string=OracleCrawler.__template_select_all_tables.substitute(
                                                                 db=oracle_database,
                                                                 user=dao.get_conn_profile_key("user")
                                                             ))

            return df_table_catalog

        except Exception as e:
            raise e

        return None
