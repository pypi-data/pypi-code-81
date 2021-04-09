# coding=utf-8

import os
from tqdm import tqdm
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import numpy as np
import tensorflow as tf
# tf.enable_eager_execution()

x = tf.Variable(tf.random.normal([1000, 20]))

index = np.random.randint(0, 1000, 20000)

import time
start_time = time.time()

@tf.function
def test():
    y = tf.gather(x, index)
    return y

for _ in tqdm(range(10000)):
    z = test()

test()

end_time = time.time()
print("elapsed: {}".format(end_time - start_time))

import tf_geometric as tfg
