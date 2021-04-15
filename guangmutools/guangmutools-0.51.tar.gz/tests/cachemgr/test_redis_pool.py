# -*- encoding: utf-8 -*-
'''
@文件    :redis_pool_test.py
@说明    :
@时间    :2021/02/23 10:25:01
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import unittest
from guangmutools.cachemgr.redispool_mgr import RedisConnector
from guangmutools.codecs_trans import Bytes2Str


class TestRedispoolConnector(unittest.TestCase):
    def setUp(self):
        print("start testing...")

    def testCacheUseful(self):
        r = RedisConnector('10.128.20.151', 6379, 9).getRedisHandler()
        r.set('foo', '9527')

        self.assertEqual('9527', Bytes2Str(r.get('foo')))