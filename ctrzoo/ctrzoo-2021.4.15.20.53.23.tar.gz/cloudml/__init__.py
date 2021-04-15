#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : __init__.py
# @Time         : 2021/2/4 5:41 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


import cloud_ml_sdk


from cloud_ml_sdk.client import CloudMlConfig, CloudMlClient

print(CloudMlClient())

print(CloudMlConfig('./cloudml.yaml')._config_data)

