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
from string import Template

import pandas as pd
from providah.factories.package_factory import PackageFactory as providah_pkg_factory

from hdc.core.catalog.rdbms_crawler import RdbmsCrawler
from hdc.core.dao.rdbms_dao import RdbmsDAO


class HiveCrawler(RdbmsCrawler):
    __template_select_all_databases = Template("SELECT DISTINCT NAME FROM DBS WHERE NAME = '$db_name'")
    __template_select_all_tables = Template("SELECT d.NAME as DATABASE_NAME, "
                                            "'$schema_name' as SCHEMA_NAME, "
                                            "t.TBL_NAME as TABLE_NAME, "
                                            "c.COLUMN_NAME as COLUMN_NAME, "
                                            "c.TYPE_NAME as COLUMN_TYPE "
                                            "FROM TBLS t "
                                            "JOIN DBS d "
                                            "ON t.DB_ID = d.DB_ID "
                                            "JOIN SDS s "
                                            "ON t.SD_ID = s.SD_ID "
                                            "JOIN COLUMNS_V2 c "
                                            "ON s.CD_ID = c.CD_ID "
                                            "WHERE d.NAME='$db_name' "
                                            "ORDER by c.INTEGER_IDX")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def obtain_catalog(self) -> pd.DataFrame:
        try:
            dao: RdbmsDAO = providah_pkg_factory.create(key=self._conf['type'].capitalize(),
                                                        library='hdc',
                                                        configuration={
                                                            'connection': self._conf['profile']})

            df_table_catalog: pd.DataFrame = self._fetch_all(dao,
                                                             query_string=HiveCrawler.__template_select_all_tables.substitute(
                                                                 schema_name='default',
                                                                 db_name=dao.get_conn_profile_key('database')))

            if not df_table_catalog.empty:
                # This had to be re-applied because the query alias doesnt seem to be working.
                # Please do not remove below mapping.
                df_table_catalog.columns = ['DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME', 'COLUMN_NAME', 'COLUMN_TYPE']

            return df_table_catalog
        except Exception as e:
            raise e

        return None
