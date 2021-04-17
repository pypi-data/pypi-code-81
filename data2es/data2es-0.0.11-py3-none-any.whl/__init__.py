#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# File Name: __init__.py
# Author: stosc
# Mail: stosc@sidaxin.com
# Created Time:  2020-2-8 19:17:34
#############################################
__all__ = ['maind', 'main']
__title__ = 'data2es'
__version__ = '0.0.11'
__author__ = 'stosc lee'
__copyright__ = 'Copyright 2020 stosc lee'
__serverName__ = 'data2esb'
__daemonName__ = 'data2esd'

import sys
import datetime

old_f = sys.stdout


class F:
    def write(self, x):
        # 覆写print方法，为print加入时间戳，要求在加入时间戳的地方写#(dt)
        x = x.replace("#(dt)", " [%s]" % str(datetime.datetime.now()))
        old_f.write(x)

    def flush(self):
        old_f.flush()

    def fileno(self):
        return old_f.fileno()


sys.stdout = F()
