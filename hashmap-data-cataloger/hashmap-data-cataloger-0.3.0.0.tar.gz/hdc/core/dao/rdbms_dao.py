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
import time
import traceback
from contextlib import contextmanager

from hdc.core.dao.dao import DAO


class RdbmsDAO(DAO):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._max_attempts = 3  # Shared property in RdbmsDAO hierarchy
        self._timeout_seconds = 10  # Shared property in RdbmsDAO hierarchy
        self.__logger = self._get_logger()

    @contextmanager
    def get_connection(self):
        """
        Obtain a context managed snowflake connection

        Returns: Snowflake connection

        Raises:
            ConnectionError: Snowflake connection could not be established

        """
        connection_established = False
        connection_attempts = 0
        timeout = self._timeout_seconds
        connection = None

        # Attempt to connect
        try:
            while connection_attempts < self._max_attempts:
                connection_profile = self._read_connection_profile(self._connection)
                connection = self._attempt_to_connect(connection_profile)

                # Test if connection has been established and break
                if self._test_connection(connection):
                    connection_established = True
                    break

                # If not, re-attempt to connect after a brief sleep
                timeout, connection_attempts = self._sleep_and_increment_counter(timeout, connection_attempts)

            if not connection_established:
                raise ConnectionError('Could not connect to the database; Exhausted connection attempts!')
        except:
            raise

        yield connection

        connection.close()

    def _test_connection(self, connection) -> bool:
        """
        Validate that the connection is valid to Snowflake instance

        Returns: True if connection is valid, False otherwise

        """
        if not connection:
            return False

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            if not len(cursor.fetchone()) > 0:
                return False

            return True

    def _sleep_and_increment_counter(self, timeout, connection_attempt_count):
        connection_attempt_count += 1
        if connection_attempt_count < self._max_attempts:
            time.sleep(self._timeout_seconds)
            timeout *= self._timeout_seconds  # TODO: sleep timeout could be increased by the same factor
        return timeout, connection_attempt_count

    def _manage_exception(self, timeout, connection_attempt_count, connection_established):
        if connection_attempt_count < self._max_attempts:
            error_message = f'Failed to connect to database; Caught exception: ' \
                            f'{traceback.format_exc()}' \
                            f'Re-attempting to connect ...'
            self.__logger.error(error_message)
            _, connection_attempt_count = self._sleep_and_increment_counter(timeout, connection_attempt_count)
        else:
            connection_established = True
        return connection_attempt_count, connection_established

    def _attempt_to_connect(self, connection_profile):
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')
