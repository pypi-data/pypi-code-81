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
# TODO: Module description
"""

import logging
import os
from functools import reduce
from pathlib import Path

from hdc.utils.file_utils import yaml_parser


class DAO:
    hds_home = 'HDS_HOME'

    def __init__(self, **kwargs):
        self.__logger = self._get_logger()
        self._connection = kwargs.get('connection')  # Shared property in DAO hierarchy

    def get_conn_profile_key(self, keys, default=None):
        """
        Fetch values for keys (nested or not) from the connection profile except the password key.
        Nested keys should be '.' delimited.

        :param keys:
        :param default:
        :return:
        """
        connection_profile = self._read_connection_profile(self._connection)
        if 'password' not in keys.split('.'):
            return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."),
                          connection_profile)
        else:
            return default

    def _get_logger(self):
        return logging.getLogger(".".join([class_type.__name__ for class_type in self.__class__.mro()[-2::-1]]))

    @staticmethod
    def _get_profile_path():
        hdc_home = Path(os.getenv(DAO.hds_home, (Path.home() / '.hdc').absolute()))
        return hdc_home / 'profile.yml'

    def _read_connection_profile(self, connection_profile_name) -> dict:
        if Path.exists(self._get_profile_path()):
            profile_yaml = yaml_parser(yaml_file_path=self._get_profile_path())

            if connection_profile_name not in profile_yaml:
                raise KeyError(f'{connection_profile_name} not configured in profile.yml')
            else:
                connection_profile = profile_yaml[connection_profile_name]  # Masking the outer local variable
        else:
            raise FileNotFoundError(
                f'Could not locate the profile.yml file. Please refer to the README for setup directions.')

        return connection_profile

    @staticmethod
    def _validate_connection_profile(profile, required_keys):
        return (all([key in profile.keys() for key in required_keys]),
                [key for key in required_keys if key not in profile.keys()])
