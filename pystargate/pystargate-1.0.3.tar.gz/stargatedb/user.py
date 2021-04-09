#!/usr/bin/ python
#coding:utf-8

"""
软件名称:星门数据库(stargateDB)
描述：星门数据库是一款微型电脑数据库
官方首页：http://www.stargatedb.com/
文档教程：http://www.stargatedb.com/index.php/wendangjiaocheng.html
申请账号：http://www.stargatedb.com/index.php/page/user.html
作者：重庆羊排信息技术有限公司
发布日期：2021年4月1日
"""
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

#查看账号
def login(username,password):
    request_url = "http://api.stargatedb.com:8002/login?username=" + str(username)+"&password="+str(password)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post( request_url,headers=headers)
    result_str = response.text
    try:
        result=eval(result_str)
        return result
    except:
        return result_str

#-----示列代码,查看账号信息-----
# res=login("xxxxx","xxxxx")
# print("用户名："+str(res['username']))
# print("密码："+str(res['password']))
# print("所有空间："+str(res['allsize'])+"KB")
# print("已用空间："+str(res['usesize'])+"KB")
# print("空闲空间："+str(res['emptysize'])+"KB")