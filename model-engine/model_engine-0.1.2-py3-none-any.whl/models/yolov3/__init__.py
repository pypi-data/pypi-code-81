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

from model_engine.models.base import RegisterModel
from model_engine.models.yolov3.base import BaseYolo, YoloRecordProvider, default_yolo_config, TinyYoloRecordProvider, \
    default_tiny_config
from model_engine.models.yolov3.models import YoloV3Tiny, YoloV3


@RegisterModel('YoloV3Tiny', 'yolov3_tiny:object_detection')
class YoloV3TinyModel(BaseYolo):
    def _get_model(self, size, training, classes):
        return YoloV3Tiny(size, training=training, classes=classes)

    class Meta:
        record_provider = TinyYoloRecordProvider
        default_configuration = default_tiny_config


@RegisterModel('YoloV3', 'yolov3:object_detection')
class YoloV3Model(BaseYolo):
    def _get_model(self, size, training, classes):
        return YoloV3(size, training=training, classes=classes)

    class Meta:
        record_provider = YoloRecordProvider
        default_configuration = default_yolo_config

