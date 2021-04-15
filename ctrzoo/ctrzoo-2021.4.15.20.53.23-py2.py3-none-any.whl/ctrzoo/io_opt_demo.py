#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : io_opt
# @Time         : 2021/2/26 11:31 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
# HDFS.HDFS_CMD = '$HADOOP_HDFS_HOME/bin/hdfs dfs'

import tensorflow as tf

from meutils.aizoo import tf_io
from meutils.decorators import hdfs_flag
from meutils.log_utils import logger4feishu

# @hdfs_flag("/user/s_feeds/yuanjie/dxx")
# def f():
#     logger4feishu("开始执行")
#
#     time.sleep(60)
#     tf_io.process_success("/user/s_feeds/yuanjie/dxx")
#
#
# f()


logger4feishu(datetime.datetime.today())
