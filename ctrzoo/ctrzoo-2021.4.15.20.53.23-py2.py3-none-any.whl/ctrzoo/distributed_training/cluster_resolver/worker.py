#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : worker
# @Time         : 2021/4/12 2:27 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
import tensorflow as tf

from meutils.pipe import *
from meutils.path_utils import get_module_path

TF_CONFIG = yaml_load(get_module_path('../TF_CONFIG.yml', __file__))
TF_CONFIG['task']['type'] = 'worker'
os.environ["TF_CONFIG"] = str(TF_CONFIG)
logger.info(TF_CONFIG)

# tf.distribute.cluster_resolver.ClusterResolver
strategy = tf.distribute.experimental.ParameterServerStrategy()
# # tf2.0需先配置cluster_resolver（即TF_CONFIG），否则报错
# import json
#
# os.environ["TF_CONFIG"] = json.dumps({
#     "cluster": {
#         "chief": ["127.0.0.1:3000"],  # 调度节点
#         "worker": ["127.0.0.1:3001"],  # 计算节点
#         "ps": ["127.0.0.1:3002"]  # 参数服务器节点，可不必使用GPU
#     },
#     "task": {"type": "worker", "index": 0}  # 定义本进程为worker节点，即["127.0.0.1:3001"]为计算节点
# })
# # 定义ParameterServerStrategy策略即可
# strategy = tf.distribute.experimental.ParameterServerStrategy()
# tf.train.ClusterSpec
# tf.distribute.MirroredStrategy
