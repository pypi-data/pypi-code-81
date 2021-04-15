# -*- encoding: utf-8 -*-
'''
@文件    :test_normal.py
@说明    :
@时间    :2021/02/23 14:16:46
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import unittest
from pprint import pprint

from guangmutools.base import project_root_path
from guangmutools.base import write_params_to_localfile, read_params_from_localfile

class TestNormalFuncs(unittest.TestCase):
    def testProjectrootpath(self):
        print(project_root_path('f:\\work\\guangmu\\ms_sensitive_check\\controllers\\utils\\admin_helpers.py', 'ms_sensitive_check', 'abc', 'def'))

    def testWriteParamsFile(self):
        ret_check = write_params_to_localfile("d:/ttt.log", {"name": "刘德华", "age": 32, "nick": "Andy Lau"})
        self.assertTrue(ret_check)

    def testReadParamsFile(self):
        data = read_params_from_localfile("d:/ttt.log")

        pprint(data)
        self.assertTrue(isinstance(data, dict))
