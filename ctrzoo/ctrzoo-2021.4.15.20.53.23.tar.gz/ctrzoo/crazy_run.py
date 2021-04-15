#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : crazy_run
# @Time         : 2021/2/26 7:09 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from ctrzoo.utils import send_device
from meutils.seize import run

send_device(__file__)


if __name__ == '__main__':
    run(1000000)
