#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/3/31 22:33   satan      1.0         This Redis is a Python library based on redis.
"""
import redis

class Redis:
    """
    :Description
    This Redis is a Python library based on redis.

    """
    def __init__(self,host :str='localhost',port: int=6379,default_db :int=0,is_decode :bool =True):
        """
        init connection
        """
        try:
            self._redis=redis.StrictRedis(host=host, port=port, db=default_db, decode_responses=is_decode)
        except BaseException as redis_connect_error:
            raise redis_connect_error

    def expire(self,key: str,num: int):
        """
        设置键值的过期时间
        :param key:键
        :param num:过期时间，单位秒
        :return:
        """
        self._redis.expire(key,num)

    def delete(self,key):
        """
        删除特定键
        :param key:要删除的键
        :return:
        """
        self._redis.delete(*key)

    def exists(self,key: str):
        """
        判断键是否存在
        :param key:要查询的键
        :return:
        """
        return self._redis.exists(key)

    def rename(self,src: str,dst: str):
        """
        重命名
        :param src:原名
        :param dst:新名字
        :return:
        """
        return self._redis.rename(src,dst)

    def reconnect(self,host :str='localhost',port: int=6379,default_db :int=0,is_decode :bool =True) -> bool:
        """

        :param host:
        :param port:
        :param default_db:
        :param is_decode:
        :return:
        """
        try:
            self._redis.close()
            self._redis=redis.StrictRedis(host=host, port=port, db=default_db, decode_responses=is_decode)
            return True
        except BaseException as redis_connect_error:
            return False

    def close(self):
        """

        :return:
        """
        self._redis.close()