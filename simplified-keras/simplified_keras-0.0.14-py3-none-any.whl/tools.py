import tensorflow as tf
import logging as log
from tensorflow.keras import mixed_precision


def allow_memory_growth():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same for all GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            log.info(f' Physical GPUs: {len(gpus)}, Logical GPUs: {len(logical_gpus)}')
        except RuntimeError as e:
            log.error(' Memory growth must be set before GPUs have been initialized')
            log.error(e)


def set_mixed_precision():
    if int(str(tf.__version__).replace('.', '')) < 241:
        from tensorflow.keras.mixed_precision.experimental import Policy, set_policy
        policy = Policy('mixed_float16')
        set_policy(policy)
    else:
        policy = mixed_precision.Policy('mixed_float16')
        mixed_precision.set_global_policy(policy)
    log.info(f' Compute dtype: {policy.compute_dtype}, variable dtype: {policy.variable_dtype}')
