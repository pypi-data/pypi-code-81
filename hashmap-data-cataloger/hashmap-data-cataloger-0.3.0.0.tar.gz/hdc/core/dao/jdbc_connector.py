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
# TODO : Module description
"""
import logging

import jaydebeapi


class JdbcConnector:

    def __init__(self, **kwargs):
        self.__logger = self._get_logger()

    @classmethod
    def connection(cls, connection_profile):
        return jaydebeapi.connect(jclassname=connection_profile['jclassname'],
                                  url=connection_profile['url'],
                                  driver_args={
                                      'user': connection_profile['user'],
                                      'password': connection_profile['password']
                                  },
                                  jars=connection_profile['jars'])

    def _get_logger(self):
        return logging.getLogger(self.__class__.__name__)
