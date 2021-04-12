# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
import requests, datetime
import pandas as pd
import numpy as np
import json
from com import *
'''Date: 2021.03.15'''


def total_handle_req(body, URL):
    response = requests.request(
        method='POST',
        url=URL,
        headers={'Content-Type': 'application/json'},
        params=None,
        data=json.dumps(body),
    )
    resp_data = response.json()
    resp_status = resp_data['success']

    if resp_status is False:
        return pd.DataFrame()
    try:
        _df_ = pd.DataFrame(resp_data['body']['data'])
    except:
        _df_ = (resp_data['body'])

    return _df_

def t_typeof(variate):
    '''返回变量的类型'''
    type = None
    if isinstance(variate, int):
        type = "int"
    elif isinstance(variate, str):
        type = "str"
    elif isinstance(variate, float):
        type = "float"
    elif isinstance(variate, list):
        type = "list"
    elif isinstance(variate, tuple):
        type = "tuple"
    elif isinstance(variate, dict):
        type = "dict"
    elif isinstance(variate, set):
        type = "set"
    return type