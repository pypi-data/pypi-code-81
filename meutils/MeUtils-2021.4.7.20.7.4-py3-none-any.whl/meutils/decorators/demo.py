#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/4/2 3:54 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.decorators.feishu import feishu_catch

from meutils.decorators import hdfs_flag

@feishu_catch()
# @feishu_hook("H")
def f():
    return 1
f()

# import time
#
# @hdfs_flag('./')
# def ff():
#     time.sleep(10)
#
#
# ff()