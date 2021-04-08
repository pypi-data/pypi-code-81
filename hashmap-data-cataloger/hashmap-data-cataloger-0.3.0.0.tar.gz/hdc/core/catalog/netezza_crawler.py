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
"""
#TODO: Module description
"""

from string import Template

import pandas as pd
from providah.factories.package_factory import PackageFactory as providah_pkg_factory

from hdc.core.catalog.rdbms_crawler import RdbmsCrawler
from hdc.core.dao.rdbms_dao import RdbmsDAO


class NetezzaCrawler(RdbmsCrawler):
    __select_all_databases = "SELECT DATABASE FROM _V_DATABASE WHERE DATABASE <> 'SYSTEM' "
    __template_select_all_schemas_in_database = Template("SELECT DISTINCT SCHEMA FROM $db_name.._V_SCHEMA ")
    __template_select_all_tables = Template("SELECT DATABASE as DATABASE_NAME, "
                                            "SCHEMA as SCHEMA_NAME, "
                                            "NAME as TABLE_NAME, "
                                            "ATTNAME as COLUMN_NAME, "
                                            "FORMAT_TYPE as COLUMN_TYPE, "
                                            "ATTLEN as COLUMN_SIZE, "
                                            "ATTNOTNULL as NOT_NULL, "
                                            "COLDEFAULT as COLUMN_DEFAULT "
                                            "FROM $db_name.._V_RELATION_COLUMN "
                                            "WHERE DATABASE <> 'SYSTEM' AND "
                                            "TYPE = 'TABLE' ORDER BY SCHEMA, NAME, ATTNUM ASC ")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def obtain_catalog(self) -> pd.DataFrame:
        try:
            dao: RdbmsDAO = providah_pkg_factory.create(key=self._conf['type'].capitalize(),
                                                        library='hdc',
                                                        configuration={
                                                            'connection': self._conf['profile']})

            df_databases = self._fetch_all(dao, NetezzaCrawler.__select_all_databases)

            df_table_catalog = []
            for db in df_databases['DATABASE'].to_list():
                df_table_catalog.extend(self._fetch_all_list(dao,
                                                             query_string=NetezzaCrawler.__template_select_all_tables
                                                             .substitute(db_name=db)))

            return pd.DataFrame(df_table_catalog)
        except:
            raise
