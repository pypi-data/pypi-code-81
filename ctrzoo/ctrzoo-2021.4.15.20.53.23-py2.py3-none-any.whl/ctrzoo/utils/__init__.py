#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : __init__.py
# @Time         : 2021/2/26 11:08 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


import tensorflow as tf
from meutils.pipe import *
from meutils.log_utils import logger4feishu

def send_device(file=''):
    """

    @param file:
    @return:
    """
    TF_VERSION = tf.__version__
    DEVICE = tf.config.list_physical_devices()
    logger4feishu(f'TF {TF_VERSION} DEVICE: {file}', '\n'.join(map(lambda x: x.name, DEVICE)))


def kinit(user='s_feeds'):
    """
    s_feeds, h_browser
    @return:
    """

    magic_cmd(f"kinit -k -t ./data/{user}.keytab {user}@XIAOMI.HADOOP")


if __name__ == '__main__':
    send_device()
