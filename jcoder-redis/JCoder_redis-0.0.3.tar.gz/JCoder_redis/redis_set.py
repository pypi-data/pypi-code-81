#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/3/31 23:01   satan      1.0         None
"""
from JCoder_redis import Redis

class r_set(Redis):
    def __init__(self,host :str='localhost',port: int=6379,default_db :int=0,is_decode :bool =True):
        """
        init
        """
        super().__init__(host,port,default_db,is_decode)

    def __getitem__(self, item: str) -> set:
        """

        :param item:
        :return:
        """
        return self._redis.smembers(item)

    def __setitem__(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        self._redis.delete(key)
        # print(type(value))
        if type(value)==tuple:
            self._redis.sadd(key,*value[0])
            self._redis.expire(key,value[1])
        else:
            self._redis.sadd(key, *value)

    def __add__(self, other:tuple) -> set :
        """

        :param other:
        :return:
        """
        return self._redis.sunion(*other)

    def ergodic(self, key,match=None,count=None):
        """

        :param key:
        :param match:
        :param count:
        :return:
        """
        return self._redis.sscan_iter(key,match,count)

    def __iand__(self, other):
        """
        other[0]=other[0]并other[1]
        :param other:
        :return:
        """
        self._redis.sunionstore(other[0],other[0],other[1])
        return self

    def __sub__(self, other) -> set :
        """
        多集合取交
        :param other:
        :return:
        """
        return self._redis.sdiff(*other)

    def __isub__(self, other):
        """

        :param other:
        :return:
        """
        self._redis.sdiffstore(other[0],other[0],other[1])
        return self

    def __and__(self, other) -> set :
        """
        多集合取并
        :param other:
        :return:
        """
        return self._redis.sinter(*other)

    def __iand__(self, other):
        """

        :param other:
        :return:
        """
        self._redis.sinterstore(other[0],other[0],other[1])
        return self

    def exist(self,keys: tuple) -> bool :
        """

        :param keys:
        :return:
        """
        if type(keys)!=tuple:
            return super().exists(keys)
        return self._redis.sismember(keys[0],keys[1])

    def __rshift__(self,other):
        """
        将成员other[2]从other[0]集合中移动到other[1]集合
        :param other:
        :return:
        """
        self._redis.smove(other[0],other[1],other[2])

    def pop(self,key: str):
        """
        随机删除并返回
        :param key:
        :return:
        """
        return self._redis.spop(key)

    def remove(self,key: str,val):
        """
        删除指定的值
        :param key:
        :param val:
        :return:
        """
        self._redis.srem(key,*val)

    def length(self,key: str) -> int :
        """

        :param key:
        :return:
        """
        return self._redis.scard(key)
