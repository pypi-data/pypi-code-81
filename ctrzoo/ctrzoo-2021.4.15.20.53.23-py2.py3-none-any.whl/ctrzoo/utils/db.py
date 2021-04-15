#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : bd
# @Time         : 2021/3/8 2:42 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

import pymysql

mysql_mitvpush_conn = pymysql.connect(
    host='10.108.231.208',
    port=6686,
    user='f2_mitvpush_x',
    passwd='REdSZkBPCtwCf6QydggvjTkRpATpFbJG',
    db='mitvpush'
)

mysql_browser_conn = pymysql.connect(
    host='10.108.231.80',
    port=6071,
    user='browser_c3_s',
    passwd='8d8b9339efef09794c8ea2267589b2bc',
    db='browser'
)

# TODO: 镜像环境
# from pyhive import hive
#
# class Hive(object):
#     """
#     sql = ""
#     df = pd.read_sql(sql, hive.conn).rename(lambda x: x.split('.')[1], axis=1)
#
#     """
#
#     @classmethod
#     def query(cls, sql=""):
#         """
#         sql='select count(1) from browser.mipush_browser_label'
#         """
#         conn = cls().conn
#         df = pd.read_sql(sql, conn).rename(lambda x: x.split('.')[1], axis=1)
#         return df
#
#     @property
#     def conn(self):
#         conn = hive.connect(
#             host="zjyprc-hadoop.hive.srv", port=10000,
#             auth="KERBEROS", kerberos_service_name="sql_prc",
#             configuration={
#                 'mapreduce.map.memory.mb': '10240',
#                 'mapreduce.reduce.memory.mb': '10240',
#                 'mapreduce.map.java.opts': '-Xmx3072m',
#                 'mapreduce.reduce.java.opts': '-Xmx3072m',
#                 'hive.input.format': 'org.apache.hadoop.hive.ql.io.HiveInputFormat',
#                 'hive.limit.optimize.enable': 'false',
#                 'mapreduce.job.queuename': 'root.production.cloud_group.feeds.pipeline',
#             },
#         )
#         return conn
