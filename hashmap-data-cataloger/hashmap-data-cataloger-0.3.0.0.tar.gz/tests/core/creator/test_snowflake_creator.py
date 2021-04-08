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

from unittest import TestCase
from unittest.mock import patch

from providah.factories.package_factory import PackageFactory as providah_pkg_factory

from hdc.core.create.creator import Creator
from hdc.core.create.snowflake_creator import SnowflakeCreator
from hdc.core.dao.dao import DAO
from hdc.core.dao.rdbms_dao import RdbmsDAO


class TestSnowflakeCreator(TestCase):

    def setUp(self) -> None:
        self._app_config = {"destinations": {
            "snowflake": {
                "type": "SnowflakeCreator",
                "conf": {
                    "type": "SnowflakeDAO",
                    "profile": "snowflake_knierr_profile"}
            }
        }
        }
        self._profiles = {
            'snowflake_knierr_profile': {
                'protocol': 'snowflake',
                'account': '< account name >',
                'role': '< snowflake role >',
                'warehouse': '< snowflake warehouse >',
                'user': '< snowflake user >',
                'password': '< user password >'
            }
        }

        self._sample_query = 'CREATE OR REPLACE TEMPORARY TABLE TEMP (COL1 VARCHAR)'

        self._creator: Creator = providah_pkg_factory.create(key=self._app_config['destinations']['snowflake']['type'],
                                                             library='hdc',
                                                             configuration={
                                                                 'conf': self._app_config['destinations']['snowflake'][
                                                                     'conf']}
                                                             )

    def test_creator_instantiation(self):
        self.assertIsNotNone(self._creator)
        self.assertIsInstance(self._creator, SnowflakeCreator)

    @patch('hdc.core.dao.snowflake.snowflake.connector')
    @patch.object(DAO, '_read_connection_profile')
    @patch.object(RdbmsDAO, '_test_connection')
    def test_replicate_structures(self, mock_test_connection, mock_read_connection_profile, mock_snowflake_connector):
        # Configure the mock object and attributes
        connection_profile = self._profiles['snowflake_knierr_profile']
        mock_read_connection_profile.return_value = connection_profile
        mock_test_connection.return_value = True
        connection_obj = mock_snowflake_connector.connect.return_value
        mock_cursor = connection_obj.cursor.return_value
        mock_cursor.execute.return_value = True

        # Execute the command to be tested
        self._creator.replicate_structures([self._sample_query])

        # Make assertions
        mock_snowflake_connector.connect.assert_called_with(**{
            'account': connection_profile['account'],
            'role': connection_profile['role'],
            'warehouse': connection_profile['warehouse'],
            'user': connection_profile['user'],
            'password': connection_profile['password'],
            'login_timeout': 30
        })

        mock_cursor.execute.assert_called_once_with(self._sample_query)
