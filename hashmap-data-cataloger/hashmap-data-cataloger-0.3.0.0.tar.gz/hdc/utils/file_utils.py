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

"""

import os
from pathlib import Path

import yaml

hds_home = 'HDS_HOME'


def yaml_parser(yaml_file_path):
    with open(yaml_file_path, 'r') as stream:
        config = yaml.safe_load(
            os.path.expandvars(
                stream.read()
            )
        )

    return config


def get_default_app_config_path():
    hdc_home = Path(os.getenv(hds_home, (Path.home() / '.hdc').absolute()))
    return hdc_home / 'hdc.yml'


def get_default_log_config_path():
    hdc_home = Path(os.getenv(hds_home, (Path.home() / '.hdc').absolute()))
    return hdc_home / 'log_settings.yml'


def get_app_config(app_config):
    # If hdc.yml is given at the CLI
    if app_config is not None:
        config_dict = yaml_parser(app_config)
    # Else read from the default location
    else:
        config_dict = yaml_parser(get_default_app_config_path())

    return config_dict
