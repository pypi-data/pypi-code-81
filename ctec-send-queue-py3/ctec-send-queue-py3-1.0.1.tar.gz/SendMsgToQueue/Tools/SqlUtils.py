# coding: utf-8
import logging
import re
import threading
import time

import mysql.connector
from DBUtils.PooledDB import PooledDB

from mysql.connector.errors import Error

logger = logging.getLogger('default')

CTEC_LAST_USE_TIME = 'ctec_last_use_time'


class IsolationLevel:
    READ_UNCOMMITTED = 'READ UNCOMMITTED'
    READ_COMMITTED = 'READ COMMITTED'
    REPEATABLE_READ = 'REPEATABLE READ'
    SERIALIZABLE = 'SERIALIZABLE'


class SqlUtils:
    sql_statement_details = dict()
    _connection_pool = None
    _idle_ping_thread = None

    @staticmethod
    def initialize_connection_pool(is_ping=True, ping_interval=30, idle_interval=60, idle_timeout=300, mincached=20,
                                   maxcached=20, maxconnections=50, db_info=None):
        SqlUtils._connection_pool = PooledDB(mysql.connector, mincached=mincached, maxcached=maxcached,
                                             maxconnections=maxconnections,
                                             **db_info)

        if is_ping:
            def ping():
                while True:
                    _condition = getattr(SqlUtils._connection_pool, '_condition')
                    _condition.acquire()
                    try:
                        idle_connections = getattr(SqlUtils._connection_pool, '_idle_cache')
                        i = 0
                        while i < len(idle_connections):
                            is_healthy = True
                            conn = idle_connections[i]
                            # 检查上次使用时间是否超过连接空闲时间设置
                            if hasattr(conn, CTEC_LAST_USE_TIME):
                                # 如果连接上次使用时间大于空闲超时时间，则会从连接池中删掉
                                if int(time.time()) - getattr(conn, CTEC_LAST_USE_TIME) > idle_timeout:
                                    if hasattr(conn, 'close'):
                                        conn.close()
                                    idle_connections.pop(i)
                                    continue
                                elif int(time.time()) - getattr(conn, CTEC_LAST_USE_TIME) <= idle_interval:
                                    # 如果小于连接空闲时间，则跳过检查
                                    i += 1
                                    continue
                            cursor = None
                            try:
                                cursor = conn.cursor()
                                cursor.execute('SELECT 1 FROM DUAL')
                                setattr(conn, CTEC_LAST_USE_TIME, int(time.time()))
                            except Error:
                                is_healthy = False
                                if hasattr(cursor, 'close'):
                                    cursor.close()
                                if hasattr(conn, 'close'):
                                    conn.close()
                                idle_connections.pop(i)
                            finally:
                                if hasattr(cursor, 'close') and is_healthy:
                                    cursor.close()
                                i += 1
                    finally:
                        _condition.release()
                    time.sleep(ping_interval)

            SqlUtils._idle_ping_thread = threading.Thread(target=ping)
            SqlUtils._idle_ping_thread.setDaemon(True)
            SqlUtils._idle_ping_thread.start()


    @staticmethod
    def get_db_connection(transaction=True, isolation_level=None, readonly=None):
        """
        获取数据库连接
        :param readonly: 事务是否只读，如果为True，则为READ ONLY，如果为False，则为READ WRITE，如果被省略，则采用数据库默认配置
        :param isolation_level: 事务隔离级别，支持'READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ',和'SERIALIZABLE'，可省略。
        :param transaction: 是否开启事务，默认开启
        :return: connection对象
        """
        logger.debug('transaction=%s, isolation_level=%s, readonly=%s', transaction, isolation_level, readonly)
        conn = SqlUtils._connection_pool.connection()
        if transaction:
            getattr(getattr(conn, '_con'), '_con').cmd_query('SET AUTOCOMMIT = 0')
        if isolation_level is not None:
            level = isolation_level.strip().replace('-', ' ').upper()
            levels = ['READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE']
            if level not in levels:
                raise ValueError('未知的 isolation level "{0}"'.format(isolation_level))
            getattr(getattr(conn, '_con'), '_con').cmd_query('SET TRANSACTION ISOLATION LEVEL {0}'.format(level))
        if readonly is not None:
            if readonly:
                access_mode = 'READ ONLY'
            else:
                access_mode = 'READ WRITE'
            getattr(getattr(conn, '_con'), '_con').cmd_query('SET TRANSACTION {0}'.format(access_mode))
        return conn

    @staticmethod
    def get_db_cursor(transaction=True, isolation_level=None, readonly=None):
        """
        获取数据库执行指针和连接
        :param readonly: 事务是否只读，如果为True，则为READ ONLY，如果为False，则为READ WRITE，如果被省略，则采用数据库默认配置
        :param isolation_level: 事务隔离级别，支持'READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ',和'SERIALIZABLE'，可省略。
        :param transaction: 是否开启事务，默认开启
        :return: conn对象,cursor对象
        """
        conn = SqlUtils.get_db_connection(transaction, isolation_level, readonly)
        cursor = conn.cursor(dictionary=True)
        return conn, cursor

    @staticmethod
    def close_all(conn, cursor):
        """
        关闭数据库游标和连接
        :param conn:
        :param cursor:
        :return:
        """
        if hasattr(cursor, 'close'):
            cursor.close()
        if hasattr(conn, 'close'):
            # 设置上次使用时间
            setattr(getattr(conn, '_con'), CTEC_LAST_USE_TIME, int(time.time()))
            conn.close()
