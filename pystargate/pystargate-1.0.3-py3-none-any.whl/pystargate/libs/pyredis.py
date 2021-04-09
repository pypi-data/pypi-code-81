#!/usr/bin/env python
# -*- coding:utf-8
import redis as pyredis

class PyRedis():
    def __init__(self):
        self._redis = pyredis.StrictRedis( 'localhost', 6379, charset="utf-8", decode_responses=True )
    #录入数据
    def Set(self,name, value,ex=None, px=None, nx=False, xx=False, keepttl=False):
        self._redis.set( name, value,ex, px, nx, xx, keepttl )

    #读取数据
    def Get(self,name):
        return self._redis.get(name)

    #删除数据
    def Delete(self,name):
        return self._redis.delete(name)

    #关闭redis
    def Close(self):
        self._redis.close()

    def Client(self):
        self._redis.client()
