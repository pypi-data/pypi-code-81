#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : multi_workers
# @Time         : 2021/4/12 8:50 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from sklearn.datasets import make_classification

from meutils.pipe import *
from meutils.log_utils import logger4feishu
magic_cmd("kinit -k -t ./data/s_feeds.keytab s_feeds@XIAOMI.HADOOP")

logger4feishu(LOCAL_HOST, os.environ["TF_CONFIG"])

strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()


def create_model():
    """from tensorflow.python.keras.models import clone_and_build_model"""
    model = Sequential()
    model.add(Dense(12, input_dim=20, kernel_initializer="uniform", activation="relu"))
    model.add(Dense(8, kernel_initializer="uniform", activation="relu"))
    model.add(Dense(1, kernel_initializer="uniform", activation="sigmoid"))
    return model


with strategy.scope():
    model = create_model()
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

X, y = make_classification(1000000, shift=0.1)

# 定义检查点（checkpoint）目录以存储检查点（checkpoints）
base_dir = 'hdfs://zjyprc-hadoop/user/s_feeds/yuanjie/cm'
log_dir = f'{base_dir}/log'
# 检查点（checkpoint）文件的名称
checkpoint_dir = f'{base_dir}/training_checkpoints'
checkpoint_prefix = f'{checkpoint_dir}/ckpt_{{epoch}}'


# 衰减学习率的函数。
# 您可以定义所需的任何衰减函数。
def decay(epoch):
    if epoch < 3:
        return 1e-3
    elif epoch >= 3 and epoch < 7:
        return 1e-4
    else:
        return 1e-5


# 在每个 epoch 结束时打印LR的回调（callbacks）。
class PrintLR(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print('\nLearning rate for epoch {} is {}'.format(epoch + 1,
                                                          model.optimizer.lr.numpy()))


callbacks = [
    tf.keras.callbacks.TensorBoard(log_dir=log_dir),
    tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix,
                                       save_weights_only=True),
    tf.keras.callbacks.LearningRateScheduler(decay),
    PrintLR()
]

model.fit(X, y, epochs=12, callbacks=callbacks)
model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

eval_loss, eval_acc = model.evaluate(X)

print('Eval loss: {}, Eval Accuracy: {}'.format(eval_loss, eval_acc))

if __name__ == '__main__':
    """一大堆业务逻辑"""


    class TEST(Main):
        @args
        def main(self, **kwargs):
            pass


    TEST.cli()
