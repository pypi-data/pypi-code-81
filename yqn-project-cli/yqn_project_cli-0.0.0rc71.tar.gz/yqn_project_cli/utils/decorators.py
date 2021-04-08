# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/12
import time
import functools
from flask import request


def parse_request_with(parser):
    def wrapper(view_func):
        @functools.wraps(view_func)
        def inner(*args, **kwargs):
            request.kwargs = parser.parse_args()
            return view_func(*args, **kwargs)

        return inner

    return wrapper


def time_it(timeout=None):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            caller = func(*args, **kwargs)
            waste = time.time() - start
            if timeout is None or (isinstance(timeout, (int, float)) and timeout < waste):
                print(func.__name__, 'waste time: %s sec' % waste)

            return caller

        return inner

    return wrapper
