#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : demo
# @Time         : 2021/4/12 2:29 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *

print(yaml_load('TF_CONFIG.yml'))

d['task']['type'] = 'worker'
