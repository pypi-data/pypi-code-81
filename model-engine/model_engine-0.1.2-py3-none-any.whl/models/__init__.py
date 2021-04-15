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

from typing import Union, Type

from model_engine.inference import BaseModelInference
from model_engine.models.base import registered_models
from model_engine.models import yolov3
from model_engine.train import BaseModelTrain


class NoSuchModel(Exception):
    pass


def get_model(model_identifier) -> Union[Type[BaseModelInference], Type[BaseModelTrain]]:
    try:
        model = registered_models[model_identifier]
        return model
    except KeyError:
        raise NoSuchModel(f'No model with identifier: {model_identifier}')
