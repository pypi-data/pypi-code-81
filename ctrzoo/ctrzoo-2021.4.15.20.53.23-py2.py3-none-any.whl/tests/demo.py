#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : demo
# @Time         : 2021/3/1 10:27 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.np_utils import normalize
from meutils.date_utils import date_difference
from meutils.log_utils import logger4feishu

from bertzoo.SimBert import SimBert
from bertzoo.utils.bert4keras_utils import texts2seq
from ctrzoo.utils.io import tf_copy_dir
import tensorflow as tf


class Config(BaseConfig):
    date = date_difference('%Y%m%d', days=1)  # 开始时间
    days = 1
    input = ''
    output = ''
    reader = ''
    writer = ''


cfg = Config.parse_zk("/mipush/common_cfg/simbert_vector")
print(cfg.date)

date = date_difference('%Y%m%d', start_date=cfg.date, days=0)
print(date)
date = date_difference('%Y%m%d', start_date=cfg.date, days=1)
print(date)
