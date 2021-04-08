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
from pandas import DataFrame

from hdc.core.catalog.crawler import Crawler


class RdbmsCrawler(Crawler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def obtain_catalog(self) -> DataFrame:
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def _fetch_all(self, dao, query_string) -> DataFrame:
        df_result_set = None
        try:
            with dao.get_connection() as conn:
                if conn is not None:
                    cursor = conn.cursor()
                    self.__logger.debug(f"Fetching data for query {query_string}")
                    cursor.execute(query_string)
                    columns = cursor.description
                    result_set = [{columns[row_index][0]: value for row_index, value in enumerate(record)} for record in
                                  cursor.fetchall()]
                    df_result_set = DataFrame(result_set)
        except:
            raise

        return df_result_set

    def _fetch_all_list(self, dao, query_string) -> list:
        df_result_set = None
        try:
            with dao.get_connection() as conn:
                if conn is not None:
                    cursor = conn.cursor()
                    self.__logger.debug(f"Fetching data for query {query_string}")
                    cursor.execute(query_string)
                    columns = cursor.description
                    df_result_set = [{columns[row_index][0]: value for row_index, value in enumerate(record)}
                                     for record in cursor.fetchall()]

        except:
            raise

        return df_result_set
