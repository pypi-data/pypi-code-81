# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/1
from threading import Lock
import pymysql
from pymysql.cursors import Cursor
from dbutils.pooled_db import PooledDB
from yqn_project_cli.rpc import RPCConfigBase
from yqn_project_cli.utils import (
    error_mark,
    warning_mark,
)


class DADictCursor(Cursor):
    dict_type = dict

    def _do_get_result(self):
        super(DADictCursor, self)._do_get_result()
        fields = []
        if self.description:
            for f in self._result.fields:
                fields.append(f.table_name + "." + f.name if f.table_name != f.org_table else f.name)

            self._fields = fields

        if fields and self._rows:
            self._rows = [self._conv_row(r) for r in self._rows]

    def _conv_row(self, row):
        if row is None:
            return None
        return self.dict_type(zip(self._fields, row))


class MySQLClient(RPCConfigBase):
    def __init__(self, **kwargs):
        super(MySQLClient, self).__init__(**kwargs)
        self.mysql_username = None
        self.mysql_password = None
        self.mysql_host = None
        self.mysql_port = None
        self.mysql_database = None
        self.mysql_charset = None

    def connect(self, **kwargs):
        if self.connector is None:
            self.mysql_username = self.server_manager.get_value('mysql_username') if self.use_conf_management \
                else self.client_config.mysql_username

            self.mysql_password = self.server_manager.get_value('mysql_password') if self.use_conf_management \
                else self.client_config.mysql_password

            self.mysql_host = self.server_manager.get_value('mysql_host') if self.use_conf_management \
                else self.client_config.mysql_host

            self.mysql_port = self.server_manager.get_value('mysql_port') if self.use_conf_management \
                else self.client_config.mysql_port

            self.mysql_database = self.server_manager.get_value('mysql_database') if self.use_conf_management \
                else self.client_config.mysql_database

            self.mysql_charset = self.server_manager.get_value('mysql_charset') if self.use_conf_management \
                else self.client_config.mysql_charset

            self.connector = PooledDB(
                creator=pymysql,
                maxconnections=6,
                mincached=2,
                maxcached=5,
                maxshared=3,
                blocking=True,
                maxusage=None,
                setsession=[],
                ping=0,
                host=self.mysql_host,
                port=int(self.mysql_port),
                user=self.mysql_username,
                password=self.mysql_password,
                database=self.mysql_database,
                charset=self.mysql_charset
            )

        connector = self.connector.connection()
        cursor = connector.cursor(cursor=kwargs.get('cursor_cls', Cursor))

        return connector, cursor

    def reconnect(self, **kwargs):
        mysql_username = kwargs.get('mysql_username', False)
        mysql_password = kwargs.get('mysql_password', False)
        mysql_host = kwargs.get('mysql_host', False)
        mysql_port = kwargs.get('mysql_port', False)
        mysql_database = kwargs.get('mysql_database', False)
        mysql_charset = kwargs.get('mysql_charset', False)

        if not all([mysql_username, mysql_password, mysql_host, mysql_port, mysql_database, mysql_charset]):
            return False

        if all([
            self.mysql_username == mysql_username,
            self.mysql_password == mysql_password,
            self.mysql_host == mysql_host,
            self.mysql_port == mysql_port,
            self.mysql_database == mysql_database,
            self.mysql_charset == mysql_charset,
        ]):
            return False

        else:
            with Lock():
                if self.connector is not None:
                    self.connector.close()
                    self.connector = None

                warning_mark('mysql is reconnecting ... ')
                print('old:', self)
                self.connect()
                print('new:', self)

            return True

    @staticmethod
    def close(connector=None, cursor=None):
        if cursor is not None:
            cursor.close()

        if connector is not None:
            connector.close()

    def fetch(self, sql, args=None, fetch_type='one', cursor_cls=Cursor):
        connector, cursor = None, None

        try:
            connector, cursor = self.connect(cursor_cls=cursor_cls)
            cursor.execute(sql, args)

        except Exception as e:
            error_mark(e)
            raise e

        else:
            if fetch_type == 'all':
                return cursor.fetchall()

            else:
                return cursor.fetchone()

        finally:
            self.close(connector, cursor)

    def fetch_all(self, sql, args=None, cursor_cls=Cursor):
        return self.fetch(sql, args, 'all', cursor_cls)

    def fetch_one(self, sql, args=None, cursor_cls=Cursor):
        return self.fetch(sql, args, 'one', cursor_cls)

    def dml_trans_handler(self, sql, args=None):
        connector, cursor = None, None

        try:
            connector, cursor = self.connect()
            _return = cursor.execute(sql, args)

        except Exception as e:
            connector.rollback()
            error_mark(e)
            raise e

        else:
            connector.commit()
            return _return

        finally:
            self.close(connector, cursor)

    def __str__(self):
        return "{user}:!password@{host}:{port}/{database}?{charset}".format(
            user=self.mysql_username,
            host=self.mysql_host,
            port=self.mysql_port,
            database=self.mysql_database,
            charset=self.mysql_charset,
        )
