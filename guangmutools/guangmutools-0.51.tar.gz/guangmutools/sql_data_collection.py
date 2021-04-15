# -*- encoding: utf-8 -*-
'''
@文件    :sql_data_collection.py
@说明    :
@时间    :2021/03/26 15:07:04
@作者    :caimmy@hotmail.com
@版本    :0.1
'''


import contextlib
import pymysql

@contextlib.contextmanager
def mysql_connector(host: str, port: int, user: str, dbname: str, pwd: str):
    conn = pymysql.connect(host=host, port=port, user=user, database=dbname, password=pwd, charset="utf8mb4")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def load_mysql_datasets(host: str, port: int, user: str, dbname: str, pwd: str, sql: str):
    with mysql_connector(host, port, user, dbname, pwd) as cursor:
        cursor.execute(sql)
        res = cursor.fetchall()
        return res
