#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/3/31 22:29   satan      1.0         None
"""
from JCoder_redis import Redis

class r_int(Redis):
    def __init__(self,host :str='localhost',port: int=6379,default_db :int=0,is_decode :bool =True):
        """
        初始化
        """
        super().__init__(host,port,default_db,is_decode)

    def __getitem__(self, item: str) -> int:
        """
        获取值
        :param item:
        :return:
        """
        return self._redis.get(item)

    def __setitem__(self, key: str, value: tuple) -> None:
        """
        设置值
        :param key:
        :param value:
        :return:
        """
        self._redis.r_set(key,value) if type(value)==int else self._redis.r_set(name=key,value=value[0],ex=value[1])

    def __iadd__(self, other: tuple):
        """
        自增
        :param other:
        :return:
        """
        self._redis.incr(other[0],other[1])
        return self