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

from contextlib import contextmanager
from dataclasses import dataclass
from typing import List


@dataclass
class Result(object):
    pass


@dataclass
class Box(object):
    __slots__ = ['x_min', 'y_min', 'x_max', 'y_max']
    x_min: int
    y_min: int
    x_max: int
    y_max: int


@dataclass
class BoundingBoxResult(object):
    __slots__ = ['label', 'confidence', 'coordinates']
    label: str
    confidence: float
    coordinates: Box


class BaseModelInference(object):
    def inference(self, image) -> List[Result]:
        pass

    @contextmanager
    def inference_session(self, labels_path, weights_path) -> 'BaseModelInference':
        try:
            return self
        finally:
            pass
