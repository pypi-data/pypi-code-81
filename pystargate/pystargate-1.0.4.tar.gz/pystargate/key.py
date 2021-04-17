#!/usr/bin/ python
#coding:utf-8

import hashlib
import requests
import time
import sys

IS_PY3 = sys.version_info.major
if IS_PY3 == 3:
    from urllib.parse import urlencode
    from urllib.parse import unquote
elif IS_PY3 == 2:
    from urllib import urlencode
    from urllib import unquote

# 查看钥匙信息
def login(username,password):
    request_url = "http://api.pystargate.com:8000/login?username=" + str(username)+"&password="+str(password)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url,headers=headers)
    result_str = response.text
    try:
        result=eval(result_str)
        return result
    except:
        return result_str

# #-----示列代码,查看钥匙信息-----
# res=login("test","123456")
# print("用户名："+str(res['username']))
# print("密码："+str(res['password']))
# print("级别："+str(res['level'])+" 级")
# print("能量："+str(res['energy'])+" 点")

# res=login("test","123456")
# # print(res)