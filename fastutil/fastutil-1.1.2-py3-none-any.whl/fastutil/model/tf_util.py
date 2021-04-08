import tensorflow as tf
import os
from fastutil.tool import gpu_util
import time


def set_gpu_and_memory(mem_required, gpu_num=1, set_memory_growth=True):
    gpu_idx_list = gpu_util.check_gpu(mem_required)
    while len(gpu_idx_list) < gpu_num:
        time.sleep(60)
        gpu_idx_list = gpu_util.check_gpu(mem_required)

    gpu_idx_list = [str(gpu_idx) for gpu_idx in gpu_idx_list]
    os.environ["CUDA_VISIBLE_DEVICES"] = ','.join(gpu_idx_list)
    if not set_memory_growth:
        return None
    if tf.__version__.startswith('1.'):
        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True
        session = tf.compat.v1.Session(config=config)
        tf.compat.v1.keras.backend.set_session(session)
        return session
    else:
        gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        return None
