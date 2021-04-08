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
# TODO : Module description
"""
import logging

from hdc.core.map import mapper_reporting


class Mapper:

    def __init__(self, **kwargs):
        self.__logger = self._get_logger()
        self._conf = kwargs.get('conf')  # Shared property in Mapper hierarchy

    def map_assets(self, df_catalog) -> list:
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def _get_logger(self):
        return logging.getLogger(".".join([class_type.__name__ for class_type in self.__class__.mro()[-2::-1]]))

    def _build_report(self, df_catalog):
        # Create and dump an HTML report of mapping summary at current working dir
        # Rename columns for cleaner reporting
        df_catalog.rename(columns={'DATABASE_NAME': 'DATABASE NAME',
                                   'SCHEMA_NAME': 'SCHEMA NAME',
                                   'TABLE_NAME': 'TABLE NAME',
                                   'COLUMN_NAME': 'COLUMN NAME',
                                   'COLUMN_TYPE': 'SOURCE DATA TYPE',
                                   'TARGET_COLUMN_TYPE': 'TARGET DATA TYPE'}, inplace=True)

        from datetime import datetime
        output_file = f"{self.__class__.__name__}_{datetime.timestamp(datetime.now())}"
        mapper_reporting.build_report_from_dataframe(df_catalog[['DATABASE NAME', 'SCHEMA NAME', 'TABLE NAME',
                                                                 'COLUMN NAME', 'SOURCE DATA TYPE',
                                                                 'TARGET DATA TYPE']],
                                                     output_file)
