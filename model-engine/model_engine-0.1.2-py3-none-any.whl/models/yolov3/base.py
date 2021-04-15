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

import contextlib
from typing import Tuple, Optional, List, Union

import tensorflow as tf

from model_engine.constants import TensorflowStrategy
from model_engine.inference import BaseModelInference, Box, BoundingBoxResult
from model_engine.models.yolov3 import dataset, utils
from model_engine.models.yolov3.models import yolo_tiny_anchors, yolo_tiny_anchor_masks, yolo_anchors, \
    yolo_anchor_masks, YoloLoss
from model_engine.train import TrainingDataProvider, BaseModelTrain, TrainingConfigProvider


class TrainingYoloRecordProvider(TrainingDataProvider):
    def __init__(self, train_path, val_path, label_map_path, size, anchors, anchor_masks):
        self.train_path = train_path
        self.val_path = val_path
        self.label_map_path = label_map_path
        self.size = size
        self.anchors = anchors
        self.anchor_masks = anchor_masks

    def training_data(self, config) -> Tuple[tf.data.Dataset, Optional[tf.data.Dataset]]:
        batch_size = config['batch_size']

        train_dataset = dataset.load_tfrecord_dataset(
            self.train_path,
            self.label_map_path,
            config,
            self.size
        )
        train_dataset = train_dataset.shuffle(buffer_size=512)
        train_dataset = train_dataset.batch(batch_size)
        train_dataset = train_dataset.map(lambda x, y: (
                dataset.transform_images(x, self.size),
                dataset.transform_targets(
                    y,
                    self.anchors,
                    self.anchor_masks,
                    self.size
                )
            )
        )
        train_dataset = train_dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

        val_dataset = dataset.load_tfrecord_dataset(
            self.val_path,
            self.label_map_path,
            config,
            self.size
        )
        val_dataset = val_dataset.batch(batch_size)
        val_dataset = val_dataset.map(lambda x, y: (
                dataset.transform_images(x, self.size),
                dataset.transform_targets(
                    y,
                    self.anchors,
                    self.anchor_masks,
                    self.size
                )
            )
        )

        return train_dataset, val_dataset


class TinyYoloRecordProvider(TrainingYoloRecordProvider):
    def __init__(self, train_path, val_path, label_map_path):
        self._anchors = yolo_tiny_anchors
        self._anchor_masks = yolo_tiny_anchor_masks
        super(TinyYoloRecordProvider, self).__init__(
            train_path,
            val_path,
            label_map_path,
            size=416,
            anchors=self._anchors,
            anchor_masks=self._anchor_masks
        )


class YoloRecordProvider(TrainingYoloRecordProvider):
    def __init__(self, train_path, val_path, label_map_path):
        self._anchors = yolo_anchors
        self._anchor_masks = yolo_anchor_masks
        super(YoloRecordProvider, self).__init__(
            train_path,
            val_path,
            label_map_path,
            size=416,
            anchors=self._anchors,
            anchor_masks=self._anchor_masks
        )


default_tiny_config = {
    'batch_size': 16,
    'training_strategy': None,
    'learning_rate': 0.001,
    'num_classes': 2,
    'transfer': 'darknet',
    'yolo_size': 416,
    'checkpoint_location': '/var/tmp/',
    'epochs': 100,
    'weights': '/var/tmp/model_data/yolov3-tiny.tf',
    'max_boxes': 100
}

default_yolo_config = {
    'batch_size': 16,
    'training_strategy': None,
    'learning_rate': 0.001,
    'num_classes': 2,
    'transfer': 'darknet',
    'yolo_size': 416,
    'checkpoint_location': '/var/tmp/',
    'epochs': 100,
    'weights': '/var/tmp/model_data/yolov3.tf',
    'max_boxes': 100
}


class BaseYolo(BaseModelTrain, BaseModelInference):
    def __init__(self):
        self._labels = None
        self._model_instance = None

    class Meta:
        record_provider = None
        default_configuration = None

    def _get_model(self, size, training, classes) -> tf.keras.Model:
        raise NotImplementedError('Must override _get_model')

    def train(self, data_provider: TrainingYoloRecordProvider,
              config_provider: Union[TrainingConfigProvider, dict] = None,
              callbacks: Optional[List[tf.keras.callbacks.Callback]] = None):
        if config_provider is None:
            config_provider = self.Meta.default_configuration

        # Unpack as many config keys possible here, reduce risk of failure later
        batch_size = config_provider['batch_size']
        strategy = config_provider['training_strategy']
        learning_rate = config_provider['learning_rate']
        num_classes = config_provider['num_classes']
        transfer_mode = config_provider['transfer']
        size = config_provider['yolo_size']
        weights = config_provider['weights']
        epochs = config_provider['epochs']

        if strategy == TensorflowStrategy.MIRRORED_STRATEGY:
            cm = tf.distribute.MirroredStrategy().scope()
        else:
            cm = contextlib.nullcontext()

        with cm:
            model = self._get_model(size, training=True, classes=num_classes)

            # Configure the model for transfer learning
            if transfer_mode == 'none':
                pass
            elif transfer_mode == 'darknet':
                model_pretrained = self._get_model(size, training=True, classes=80)
                model_pretrained.load_weights(weights)  # TODO: Find better way to handle base weight files

                model.get_layer('yolo_darknet').set_weights(
                    model_pretrained.get_layer('yolo_darknet').get_weights()
                )
                utils.freeze_all(model.get_layer('yolo_darknet'))

            optimizer = tf.keras.optimizers.Adam(lr=learning_rate)
            loss = [
                YoloLoss(data_provider.anchors[mask], classes=num_classes) for mask in data_provider.anchor_masks
            ]

            # XXX: Stripped out support for eager_tf

            model.compile(
                optimizer=optimizer,
                loss=loss,
                run_eagerly=False
            )

            training_data, validation_data = data_provider.training_data(config_provider)

            history = model.fit(
                training_data,
                epochs=epochs,
                callbacks=callbacks,
                validation_data=validation_data
            )

            return history

    def _can_inference_check(self):
        if self._model_instance is None:
            # TODO: Custom exception type
            raise Exception('Model is not loaded. Do not call inference outside a session.')

    def _load_model(self, labels_path: str, weights_path: str) -> Tuple[List[str], tf.keras.Model]:
        try:
            with open(labels_path, 'r') as labels_file:
                label_data = labels_file.readlines()
            labels = [label.strip() for label in label_data]
        except FileNotFoundError:
            raise  # TODO: possibly better error handling here

        try:
            model_instance = self._get_model(size=None, training=False, classes=len(labels))
            model_instance.load_weights(weights_path).expect_partial()
            return labels, model_instance
        except Exception:
            raise  # TODO: definitely better error handling here

    def inference(self, image):
        self._can_inference_check()

        img_raw = tf.image.decode_image(image)
        height, width, channels = img_raw.shape
        img = tf.expand_dims(img_raw, 0)
        img = dataset.transform_images(img, 416)  # TODO: Replace magic number w/ correct model size

        boxes, scores, classes, nums = self._model_instance.predict(img)
        boxes, scores, classes, nums = boxes[0], scores[0], classes[0], nums[0]

        results = []
        for idx, box in enumerate(boxes):
            score = scores[idx].item()
            if score == 0:
                continue
            label = self._labels[int(classes[idx])]
            x_min = box[0].item() * width
            y_min = box[1].item() * height
            x_max = box[2].item() * width
            y_max = box[3].item() * height
            box = Box(x_min, y_min, x_max, y_max)
            result = BoundingBoxResult(label, score, box)
            results.append(result)
        return results

    def inference_file(self, image_path):
        self._can_inference_check()

        with open(image_path, 'rb') as image_file:
            return self.inference(image_file.read())

    @contextlib.contextmanager
    def inference_session(self, labels_path, weights_path):
        try:
            self._labels, self._model_instance = self._load_model(labels_path, weights_path)
            yield self
        finally:
            self._model_instance = None
