#  Copyright 2020 BlueChasm LLC dba OsmosisAI.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import enum


class TensorflowStrategy(enum.Enum):
    MIRRORED_STRATEGY = 'MirroredStrategy'
    TPU_STRATEGY = 'TPUStrategy'
    MULTI_WORKER_STRATEGY = 'MultiWorkerMirroredStrategy'
    CENTRAL_STORAGE_STRATEGY = 'CentralStorageStrategy'
    PARAMETER_SERVER_STRATEGY = 'ParameterServerStrategy'
    ONE_DEVICE_STRATEGY = 'OneDeviceStrategy'
