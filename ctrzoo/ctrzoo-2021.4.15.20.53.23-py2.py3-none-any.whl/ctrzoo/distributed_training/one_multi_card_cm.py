#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : one_multi_card
# @Time         : 2021/4/12 8:02 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


import tensorflow as tf
import tensorflow_datasets as tfds

from meutils.pipe import *

tfds.disable_progress_bar()
magic_cmd("kinit -k -t ./data/s_feeds.keytab s_feeds@XIAOMI.HADOOP")

datasets, info = tfds.load(name='mnist', with_info=True, as_supervised=True)
mnist_train, mnist_test = datasets['train'], datasets['test']

strategy = tf.distribute.MirroredStrategy()
print('Number of devices: {}'.format(strategy.num_replicas_in_sync))

# 您还可以执行 info.splits.total_num_examples 来获取总数
# 数据集中的样例数量。

num_train_examples = info.splits['train'].num_examples
num_test_examples = info.splits['test'].num_examples

BUFFER_SIZE = 10000

BATCH_SIZE_PER_REPLICA = 64
BATCH_SIZE = BATCH_SIZE_PER_REPLICA * strategy.num_replicas_in_sync


def scale(image, label):
    image = tf.cast(image, tf.float32)
    image /= 255

    return image, label


train_dataset = mnist_train.map(scale).cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
eval_dataset = mnist_test.map(scale).batch(BATCH_SIZE)

with strategy.scope():
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10)
    ])

    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  optimizer=tf.keras.optimizers.Adam(),
                  metrics=['accuracy'])

# 定义检查点（checkpoint）目录以存储检查点（checkpoints）
base_dir = 'hdfs://zjyprc-hadoop/user/s_feeds/yuanjie/cm'
log_dir = f'{base_dir}/log'
# 检查点（checkpoint）文件的名称
checkpoint_dir = f'{base_dir}/training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")


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

model.fit(train_dataset, epochs=12, callbacks=callbacks)
model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

eval_loss, eval_acc = model.evaluate(eval_dataset)

print('Eval loss: {}, Eval Accuracy: {}'.format(eval_loss, eval_acc))

if __name__ == '__main__':
    """一大堆业务逻辑"""


    class TEST(Main):
        @args
        def main(self, **kwargs):
            pass


    TEST.cli()
