#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/3/31 22:33   satan      1.0         None
"""
from JCoder_redis import Redis

class r_list(Redis):
    def __init__(self,host :str='localhost',port: int=6379,default_db :int=0,is_decode :bool =True):
        """
        init
        """
        super().__init__(host,port,default_db,is_decode)

    def __getitem__(self, item: tuple):
        """
        获取值
        :param item:
        :return:
        """
        if type(item)==tuple:
            return self._redis.lindex(item[0],item[1])
        else:
            return self._redis.lrange(item,0,-1)

    def __setitem__(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        if type(key)==str:
            self._redis.delete(key)
            if type(value)==tuple:
                self._redis.rpush(key,*value[0])
                self._redis.expire(key,value[1])
            else:
                self._redis.rpush(key, *value[0])
        else:
            self._redis.lset(key[0],key[1],value)

    def __iadd__(self, other: tuple):
        """

        :param other:
        :return:
        """
        self._redis.rpush(other[0],*other[1])
        return self

    def length(self,key: str) -> int :
        """
        获取长度
        :param key:
        :return:
        """
        return self._redis.llen(key)

    def push_front(self, key,value):
        """
        从前添加
        :param key:
        :param value:
        :return:
        """
        self._redis.lpush(key,*value)
        return self

    def insert_before(self,key,num,value):
        """
        在num前插入value，注意此处的num是指数组中的值，不是下标
        :param key:
        :param num:
        :param value:
        :return:
        """
        self._redis.linsert(key,"before",num,value)

    def insert_after(self,key,num,value):
        """

        :param key:
        :param num:
        :param value:
        :return:
        """
        self._redis.linsert(key,"after",num,value)

    def remove(self,key,index,num):
        """
        删除对应值的元素
        :param key:
        :param index:
        :param num:删除的个数，0：全部，>0从前向后的num个，<0从后向前的num个
        :return:
        """
        self._redis.lrem(key,index,num)

    def pop_front(self,key):
        """
        删除并返回第一个值
        :param key:
        :return:
        """
        return self._redis.lpop(key)

    def pop_back(self,key):
        """
        删除并返回第二个值
        :param key:
        :return:
        """
        return self._redis.rpop(key)

    def remain_range(self,key: str,start: int,end: int):
        """
        删除索引以外的值
        :param key:
        :param start:
        :param end:
        :return:
        """
        return self._redis.lrange(key,start,end)

    def __rshift__(self, other):
        """
        从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边
        :param other:
        :return:
        """
        self._redis.rpoplpush(other[0],other[1])

    def remove_lists(self,keys):
        """
        批量删除list
        :param keys:
        :return:
        """
        self._redis.blpop(*keys)

    def ergodic(self,key: str,_from: int=0,_to: int=-1):
        """
        自定义增量迭代器
        :param key:
        :param _from:
        :param _to:
        :return:
        """
        if _to<0:
            _to=self.length(key)
        for index in range(_from,_to):
            yield self._redis.lindex(key,index)