from pathlib import Path
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
import random
import tensorflow as tf


# tran data has to be in train folder and validation data has to be in val folder
from typing import Tuple


def get_train_val_generators(img_datagen: ImageDataGenerator, data_dir='../data', color_mode='rgb',
                             batch_size=128, class_mode='categorical', **kwargs):
    train_generator = img_datagen.flow_from_directory(os.path.join(data_dir, 'train'),
                                                      batch_size=batch_size,
                                                      color_mode=color_mode,
                                                      class_mode=class_mode,
                                                      **kwargs)
    validation_generator = img_datagen.flow_from_directory(os.path.join(data_dir, 'val'),
                                                           batch_size=batch_size,
                                                           color_mode=color_mode,
                                                           class_mode=class_mode,
                                                           **kwargs)
    return train_generator, validation_generator


def get_val_test_generators(img_datagen: ImageDataGenerator, data_dir='../data', color_mode='rgb',
                            batch_size=128, class_mode='categorical', **kwargs):
    validation_generator = img_datagen.flow_from_directory(os.path.join(data_dir, 'val'),
                                                           batch_size=batch_size,
                                                           color_mode=color_mode,
                                                           class_mode=class_mode,
                                                           **kwargs)

    test_generator = img_datagen.flow_from_directory(os.path.join(data_dir, 'test'),
                                                     batch_size=batch_size,
                                                     color_mode=color_mode,
                                                     class_mode=class_mode,
                                                     **kwargs)
    return validation_generator, test_generator


def numpy_memmap_generator(x_path: Path, y_path: Path, batch_size: int = 128, shuffle_array: bool = True):
    while True:
        x = np.load(x_path, mmap_mode='r')
        y = np.load(y_path, mmap_mode='r')
        indexes = [i for i in range(x.shape[0])]

        if shuffle_array:
            random.shuffle(indexes)

        iterations = len(indexes) // batch_size + 1
        for i in range(iterations):
            slice_begin = i * batch_size
            slice_end = (i + 1) * batch_size
            slice_indexes = indexes[slice_begin: slice_end]
            yield x[slice_indexes], y[slice_indexes]


def get_train_val_image_datasets(train_path: Path, val_path: Path, image_size: Tuple[int, int], batch_size: int = 64,
                                 label_mode: str = 'categorical', cache_train: bool = False, cache_val: bool = True,
                                 **kwargs):
    # loading is on CPU so should be float32 (faster than float16),
    # it will be casted on first model layer to float16 on GPU
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(train_path,
                                                                   label_mode=label_mode,
                                                                   batch_size=batch_size,
                                                                   image_size=image_size,
                                                                   **kwargs)

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(val_path,
                                                                 label_mode=label_mode,
                                                                 batch_size=batch_size,
                                                                 image_size=image_size,
                                                                 shuffle=False,
                                                                 **kwargs)

    train_ds = train_ds.cache().prefetch(tf.data.AUTOTUNE) if cache_train else train_ds.prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.cache().prefetch(tf.data.AUTOTUNE) if cache_val else val_ds.prefetch(tf.data.AUTOTUNE)
    return train_ds, val_ds
