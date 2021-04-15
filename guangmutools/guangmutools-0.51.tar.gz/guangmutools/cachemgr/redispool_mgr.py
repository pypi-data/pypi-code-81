# -*- encoding: utf-8 -*-
'''
@文件    :redispool.py
@说明    :
@时间    :2021/02/23 10:21:39
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import redis


class RedisConnector(object):
    def __init__(self, host, port, db=1):
        self._pool = redis.ConnectionPool(host=host, port=port, db=db)

    def getRedisHandler(self) -> redis.Redis:
        return redis.Redis(connection_pool=self._pool)