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

import snowflake.connector

from hdc.core.dao.rdbms_dao import RdbmsDAO


class SnowflakeDAO(RdbmsDAO):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def _attempt_to_connect(self, connection_profile):
        # Assume Snowflake connector type if protocol property not set
        # within connection profile
        protocol = connection_profile.get('protocol', 'snowflake').lower()

        if protocol == "snowflake":
            return SnowflakeDAO.__snowflake_connector(connection_profile)

        return None

    @staticmethod
    def __snowflake_connector(connection_profile):

        auth_type1_present = RdbmsDAO._validate_connection_profile(connection_profile,
                                                                   ['account', 'role', 'warehouse', 'user', 'password'])

        if not auth_type1_present[0]:
            auth_type2_present = RdbmsDAO._validate_connection_profile(connection_profile,
                                                                       ['account', 'role', 'warehouse', 'user',
                                                                        'authenticator'])

            if not auth_type2_present[0]:
                raise KeyError(f'One or more of {auth_type1_present[1] + auth_type2_present[1]} keys '
                               f'not configured in profile')
            else:
                kwrgs = {
                    'account': connection_profile['account'],
                    'role': connection_profile['role'],
                    'warehouse': connection_profile['warehouse'],
                    'user': connection_profile['user'],
                    'authenticator': connection_profile['authenticator'],
                    'login_timeout': 30
                }
        else:
            kwrgs = {
                'account': connection_profile['account'],
                'role': connection_profile['role'],
                'warehouse': connection_profile['warehouse'],
                'user': connection_profile['user'],
                'password': connection_profile['password'],
                'login_timeout': 30
            }

        if 'database' in connection_profile:
            kwrgs['database'] = connection_profile['database']

            if 'schema' in connection_profile:
                kwrgs['schema'] = connection_profile['schema']

        return snowflake.connector.connect(**kwrgs)
