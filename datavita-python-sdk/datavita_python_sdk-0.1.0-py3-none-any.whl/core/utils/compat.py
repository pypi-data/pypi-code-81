# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : compat.py
    @desc :
"""
import sys

PY3 = sys.version_info[0] == 3

if PY3:
    str = str
    string_types = (str,)
    from collections.abc import Callable
else:
    import types

    str = unicode  # noqa: F821
    string_types = types.StringTypes

    from collections import Callable
