#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/3/31 22:33   satan      1.0         None
"""
from JCoder_redis import Redis

class r_dict(Redis):
    def __init__(self,host :str='localhost',port: int=6379,default_db :int=0,is_decode :bool =True):
        """
        init
        """
        super().__init__(host,port,default_db,is_decode)

    def __getitem__(self, item:tuple):
        """
        获取对象
        :param item:如果item是tuple类型，则返回item[0]->{item[1]:(return)}，否则返回item->(return)
        :return:
        """
        if type(item)==tuple:
            return self._redis.hget(item[0],item[1])
        else:
            return self._redis.hgetall(item)

    def __setitem__(self, key:tuple , value):
        """
        设置对象
        :param key:key[0]主键，key[1]内部键
        :param value:value[0]值，value[1]过期时间
        :return:
        """
        if type(key)==tuple:
            self._redis.hset(key[0], key[1], value)
        else:
            if type(value) == tuple:
                self._redis.hmset(key,value[0])
                self._redis.expire(key,value[1])
            else:
                self._redis.hmset(key,value)

    def get_items(self,key:str, items: list) -> list:
        """
        批量获取对象
        :param key:主键
        :param items:内部键，为数组类型
        :return:
        """
        return self._redis.hmget(key,items)

    def get_keys(self,key: str) -> list:
        """
        得到内部键
        :param key:主键
        :return:
        """
        return self._redis.hkeys(key)

    def get_values(self,key: str) -> list:
        """
        得到内部值
        :param key:主键
        :return:
        """
        return self._redis.hvals(key)

    def length(self,key: str) -> int:
        """
        字典长度
        :param key:主键
        :return:
        """
        return self._redis.hlen(key)

    def exists(self,name:str,key:str) -> bool:
        """
        判断给定键是否存在
        :param name:主键
        :param key:内部键
        :return:
        """
        return self._redis.hexists(name,key)

    def __delitem__(self, key:tuple):
        """
        删除元素
        :param key:key[0]主键,key[1]内部键
        :return:
        """
        self._redis.hdel(key[0],*key[1])

    def __iadd__(self, other: tuple):
        """
        自增，内部键对应的类型必须为int或float
        :param other:other[0]主键,other[1]内部键,other[2]增幅
        :return:
        """
        self._redis.hincrby(other[0],other[1],other[2]) if type(other[2])==int else self._redis.hincrbyfloat(other[0],other[1],other[2])

    def get_range(self,name:str,cursor :int=0,match=None,count: int=None):
        """
        切片
        :param name:
        :param cursor:
        :param match:
        :param count:
        :return:
        """
        return self._redis.hscan(name,cursor,match,count)

    def ergodic(self,name:str,match=None,count=None):
        """
        迭代器遍历
        :param name:
        :param match:
        :param count:
        :return:
        """
        return self._redis.hscan_iter(name,match,count)
            # yield i

