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

from hdc.core.dao.jdbc_connector import JdbcConnector
from hdc.core.dao.odbc_connector import OdbcConnector
from hdc.core.dao.rdbms_dao import RdbmsDAO


class Netezza(RdbmsDAO):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def _attempt_to_connect(self, connection_profile):
        """

        :param connection_profile:
        :return:
        """

        # Assume JDBC connector type if protocol property not set
        # within connection profile
        protocol = connection_profile.get('protocol', 'jdbc').lower()

        if protocol == "jdbc":
            return Netezza.__jdbc_connector(connection_profile)
        elif protocol == "odbc":
            return Netezza.__odbc_connector(connection_profile)

        return None

    @staticmethod
    def __odbc_connector(connection_profile):
        base_keys_validation_output = RdbmsDAO._validate_connection_profile(connection_profile,
                                                                            ['user', 'password', 'host', 'port',
                                                                             'database', 'driver'])

        if base_keys_validation_output[0]:
            driver_keys_validation_output = RdbmsDAO._validate_connection_profile(connection_profile['driver'],
                                                                                  ['name'])
            if not driver_keys_validation_output[0]:
                raise KeyError(
                    f'One or more of {driver_keys_validation_output[1]} keys not configured in profile')
        else:
            raise KeyError(
                f'One or more of {base_keys_validation_output[1]} keys not configured in profile')

        return OdbcConnector.connection({
            "driver": connection_profile['driver']['name'],
            "connection_string": f"DRIVER={connection_profile['driver']['name']};SERVER={connection_profile['host']};"
                                 f"PORT={connection_profile['port']};DATABASE={connection_profile['database']};"
                                 f"UID={connection_profile['user']};PWD={connection_profile['password']};"
        })

    @staticmethod
    def __jdbc_connector(connection_profile):
        base_keys_validation_output = RdbmsDAO._validate_connection_profile(connection_profile,
                                                                            ['user', 'password', 'host', 'port',
                                                                             'database', 'driver'])

        if base_keys_validation_output[0]:
            driver_keys_validation_output = RdbmsDAO._validate_connection_profile(connection_profile['driver'],
                                                                                  ['name', 'path'])
            if not driver_keys_validation_output[0]:
                raise KeyError(
                    f'One or more of {driver_keys_validation_output[1]} keys not configured in profile')
        else:
            raise KeyError(
                f'One or more of {base_keys_validation_output[1]} keys not configured in profile')

        # If all required properties are available, get a new connection to the Netezza database
        return JdbcConnector.connection({
            "jclassname": connection_profile['driver']['name'],
            "jars": connection_profile['driver']['path'],
            "url": f"jdbc:netezza://{connection_profile['host']}:{connection_profile['port']}/{connection_profile['database']}",
            "user": connection_profile['user'],
            "password": connection_profile['password']
        })
