# Copyright © 2021 Hashmap, Inc
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
import os
from typing import Optional

from providah.factories.package_factory import PackageFactory as pf
import yaml
from fastapi import FastAPI
from pydantic import BaseModel

from deployz.executors.executor import Executor


def get_servz() -> Executor:
    config: dict = get_configuration()
    servz_config = config['servz']
    registry = pf.create(key=servz_config['artifact_registry']['name'],
                         configuration=servz_config['artifact_registry']['conf'])
    executor_config = servz_config['executor']['conf']
    executor_config['registry'] = registry
    executor = pf.create(key=servz_config['executor']['name'],
                         configuration=executor_config)

    return executor


def get_autotrainz() -> Executor:
    config: dict = get_configuration()
    autotrainz_config = config['autotrainz']
    registry = pf.create(key=autotrainz_config['artifact_registry']['name'],
                         configuration=autotrainz_config['artifact_registry']['conf'])
    executor_config = autotrainz_config['executor']['conf']
    executor_config['registry'] = registry
    executor = pf.create(key=autotrainz_config['executor']['name'],
                         configuration=executor_config)

    return executor


def get_configuration() -> dict:
    path = os.getenv('DEPLOYZ_CONF')
    if not path:
        path = 'deployz.yml'

    with open(path, 'r') as stream:
        configuration = yaml.safe_load(stream)

    return configuration
