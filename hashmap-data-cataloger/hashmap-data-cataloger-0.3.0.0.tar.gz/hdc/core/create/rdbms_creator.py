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
# TODO: Module description
"""

import pandas as pd

from hdc.core.create.creator import Creator


class RdbmsCreator(Creator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def replicate_structures(self, sql_ddl_list):
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def _fetch_all(self, dao, query_string, column_map) -> pd.DataFrame:
        try:
            with dao.get_connection() as conn:
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute(query_string)
                    df = cursor.fetch_pandas_all()
                    df.columns = list(column_map.keys())
                    return df
                else:
                    return None
        except:
            raise

    def _stream_result_set(self, dao, query_string) -> pd.DataFrame:
        try:
            with dao.get_connection() as conn:
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute(query_string)
                    for df in cursor.fetch_pandas_batches():
                        yield df
                else:
                    return None
        except:
            raise

    def _execute_update(self, dao, query_list):
        try:
            with dao.get_connection() as conn:
                if conn is not None:
                    cursor = conn.cursor()
                    for sql in query_list:
                        cursor.execute(sql)
        except:
            raise
