# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : encoder.py
    @desc :
"""
from datavita.core.utils.compat import str


def encode(d: dict) -> dict:
    result = {}

    for k, v in d.items():
        if isinstance(v, dict):
            for ek, ev in encode(v).items():
                result["{}.{}".format(k, ek)] = encode_value(ev)
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    for ek, ev in encode(item).items():
                        result["{}.{}.{}".format(k, i, ek)] = encode_value(ev)
                else:
                    result["{}.{}".format(k, i)] = encode_value(item)
        else:
            result[k] = encode_value(v)

    return result


def encode_value(v):
    # bool only accept lower case
    if isinstance(v, bool):
        return "true" if v else "false"

    # api gateway will try to decode float as int in lua syntax
    if isinstance(v, float):
        return str(int(v)) if v % 1 == 0 else str(v)

    return str(v)
