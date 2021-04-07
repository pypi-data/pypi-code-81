# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       utils
   Description :
   Author:          蒋付帮
   date:            2019-10-28 16:32
-------------------------------------------------
   Change Activity:
                    2021-03-12: 代码优化/功能更新
                    2021-03-15：功能更新
                    2021-03-29：功能更新: get_now_datetime()
-------------------------------------------------
"""
__author__ = 'jiangfb'

import datetime
import math
from datetime import datetime as dt
from datetime import timedelta


def headers_str_to_dict(headers_str: str) -> dict:
    """
    headers字符串格式转字典格式
    :param headers_str: headers字符串格式
    :return: headers字典格式
    """
    lines = headers_str.split("\n")
    headers = dict()
    for line in lines:
        if line.strip():
            key, value = line.split(": ")
            headers[key.strip()] = value.strip()
    return headers

def timestamp_to_localtime(timestamp, _format="%Y-%m-%d %H:%M:%S") -> str:
    """
    时间戳转格式化字符串类型
    :param timestamp: 字符串或整形型时间戳(10/13位均可)
    :param _format: 格式
    :return: localtime类型
    """
    if isinstance(timestamp, str):
        if len(timestamp) == 13:
            timestamp = int(timestamp[:-3])
        else:
            timestamp = int(timestamp)
    elif isinstance(timestamp, int):
        if len_int(timestamp) == 13:
            timestamp = timestamp / 1000
    timeArray = datetime.datetime.fromtimestamp(timestamp)
    return timeArray.strftime(_format)

def localtime_to_datetime(localtime: str, _format='%Y-%m-%d %H:%M:%S') -> datetime:
    """
    时间格式字符串转datetime类型
    :param localtime: 本地时间格式字符串
    :param _format: 格式
    :return: datetime格式
    """
    return datetime.datetime.strptime(localtime, _format)

def timestamp_to_datetime(timestamp) -> datetime:
    """
    时间戳转datetime格式
    :param timestamp: 字符串或整形型时间戳(10/13位均可)
    :return: datetime格式
    """
    return localtime_to_datetime(timestamp_to_localtime(timestamp))

def get_delta_datetime(days: float) -> datetime:
    """
    获取指定时间前的日期
    :param days: 间隔的时间天数
    :return: days天前的日期
    """
    now = dt.now()
    if days < 0:
        delta = timedelta(days=abs(days))
        n_days_forward = now - delta
    else:
        delta = timedelta(days=days)
        n_days_forward = now + delta
    return n_days_forward

def get_now_datetime() -> datetime:
    """
    获取当前时间-datetime格式
    :return: 当前时间
    """
    return datetime.datetime.now()

def len_int(n: int) -> int:
    """
    返回数字长度
    :param n: 输入数字
    :return: 数字长度
    """
    if n > 0:
        digits = int(math.log10(n)) + 1
    elif n == 0:
        digits = 1
    else:
        digits = int(math.log10(-n)) + 2
    return digits

if __name__ == '__main__':
    print(get_delta_datetime(0))