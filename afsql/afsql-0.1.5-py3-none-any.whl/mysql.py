# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     mysql
   Description :
   Author :        Asdil
   date：          2021/4/1
-------------------------------------------------
   Change Activity:
                   2021/4/1:
-------------------------------------------------
"""
__author__ = 'Asdil'
from dbutils.persistent_db import PersistentDB
from dbutils.pooled_db import PooledDB
import pymysql


class Mysql:
    """
    Mysql类用于mysql连接池操作
    """
    def __init__(self, host, port, user, password, database, pool=1):
        """__init__(self):方法用于

        Parameters
        ----------
        host : str
            host地址
        port : int
            端口
        user : str
            用户名
        password : str
            密码
        database : str
            数据库名称

        Returns
        ----------
        """
        if pool == 0:
            self.pool = PersistentDB(
                creator=pymysql,  # 使用连接数据库模块
                maxusage=None,  # 连接超时时间
                setsession=[],  # 开始会话前执行的操作
                ping=0,  # ping服务器端查看是否可用
                closeable=False,  # 实际上被忽略，供下次使用，再线程关闭时，才会自动关闭链接。如果为True时， conn.close()则关闭链接，
                # 那么再次调用pool.connection时就会报错，因为已经真的关闭了连接（pool.steady_connection()可以获取一个新的链接
                threadlocal=None,  # 本线程独享值得对象，用于保存链接对象，如果链接对象被重置
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset='utf8')
        else:
            self.pool = PooledDB(
                creator=pymysql,  # 使用连接数据库模块
                maxusage=None,  # 连接超时时间
                setsession=[],  # 开始会话前执行的操作
                ping=1,  # ping服务器端查看是否可用
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset='utf8')

    def select_one(self, sql, args=None):
        """select_one方法用于查询一条数据

        Parameters
        ----------
        sql : str
            sql 语句
        args : list or tuple
            参数
        Returns
        ----------
        """
        conn = self.pool.connection(shareable=False)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def select_all(self, sql, args=None):
        """select_all方法用于查询所有数据

        Parameters
        ----------
        sql : str
            sql 语句
        args : list or tuple or None
            参数
        Returns
        ----------
        """
        if args:
            args = tuple(args)
        conn = self.pool.connection(shareable=False)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        conn.close()
        return result

    def excute(self, sql, args=None):
        """excute方法用于增删查改

        Parameters
        ----------
        param : str

        Returns
        ----------
        """
        if args:
            args = tuple(args)
        conn = self.pool.connection(shareable=False)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        conn.commit()
        conn.close()


def optimize_expression(sql, params):
    """optimize_expression方法用于优化sql表达式
    使用方法:
        sql = "select * from table1 where age=%s and name in (%s)"
        params = [10, ['Tom', 'Jim']]
        sql, params = optimize_expression(sql, params)
    Parameters
    ----------
    sql : str
        sql语句
    params ： 参数列表

    Returns
    ----------
    """
    new_params = []
    codes = []
    for param in params:
        if isinstance(param, list):
            new_params.extend(list(map(str, param)))
            codes.append(','.join(['%s']*len(param)))
        else:
            new_params.append(param)
            codes.append('%s')
    sql = sql % tuple(codes)
    return sql, new_params


if __name__ == '__main__':
    db = Mysql(host='127.0.0.1', port=3306, user='root', password='', database='mysql')
    data = db.select_all("show tables;")
    print(data)
