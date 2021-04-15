# -*- encoding: utf-8 -*-
'''
@文件    :decorators.py
@说明    :
@时间    :2021/02/23 10:13:06
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

from functools import wraps


def singleton(cls):
    '''
    单例装饰器
    '''
    _instance = {}

    @wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _singleton