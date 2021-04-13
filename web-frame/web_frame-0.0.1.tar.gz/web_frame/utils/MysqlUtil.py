import os

import pymysql
import logging
import traceback

from web_frame.context import config
from web_frame.utils.DBUtil import BaseSession
from web_frame.utils.FileUtil import read_text


def mysql_connect(host, user, port, db, pwd):
    if not db:
        db = config.mysql_database
    if not host:
        host = config.mysql_ip
    if not user:
        user = config.mysql_user
    if not port:
        port = config.mysql_port
    if not pwd:
        pwd = config.mysql_password
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            port=port,
            database=db,
            password=pwd,
            # auth_plugin='mysql_native_password',
            charset="utf8"
        )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        logging.warning("连接数据库异常:" + traceback.format_exc())
        return "", str(e)


def create_table(sql_file):
    table = sql_file.split(os.path.sep)[-1].replace(".sql", "")
    sql = "select count(*) from information_schema.tables where table_schema='{}' and table_name = '{}'".format(
        config.mysql_database, table)
    with SqlSession() as session:
        exist = session.query_one(sql, "object")
        if exist == 0:
            create_sql = read_text(sql_file)
            session.execute_update(create_sql.strip())


class SqlSession(BaseSession):
    def __init__(self, host=None, user=None, port=None, db=None, pwd=None, auto_commit=True):
        super().__init__(auto_commit)
        self.conn, self.cursor = mysql_connect(host, user, port, db, pwd)
        self.protocol = "mysql"
        if self.conn == "":
            raise Exception(self.cursor)
