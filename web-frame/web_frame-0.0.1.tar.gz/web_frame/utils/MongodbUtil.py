import logging
import traceback

from pymongo import MongoClient

from web_frame.context import config
from web_frame.utils.CommonUtil import is_empty
from web_frame.utils.DBUtil import BaseSession


def mongodb_connect(db, host, port, user, pwd):
    if not db:
        db = config.mongo_database
    if not host:
        host = config.mongo_ip
    if not user:
        user = config.mongo_user
    if not port:
        port = config.mongo_port
    if not pwd:
        pwd = config.mongo_password
    try:
        client = MongoClient(host, int(port))
        db_obj = client.admin  # 先连接系统默认数据库admin
        db_obj.authenticate(user, pwd, mechanism='SCRAM-SHA-1')
        db_obj = client[db]
        return db_obj, client
    except Exception as e:
        logging.warning("连接数据库异常:" + traceback.format_exc())
        return "", str(e)


def convert_to_mongo(value):
    if isinstance(value, str) and not is_empty(value):
        if (value[0] == "'" and value[-1] == "'") or (value[0] == '"' and value[-1] == '"'):
            return value
        else:
            return "'" + value + "'"
    elif isinstance(value, list):
        result = "[{}]"
        temp_list = []
        for item in value:
            temp_list.append(convert_to_mongo(item))
        return result.format(",".join(temp_list))
    return str(value)


def prepare_for_mongo(params: dict):
    result = {}
    for key, value in params.items():
        result[key] = convert_to_mongo(value)
    return result


def query_params_for_mongo(db, query: str, params=None):
    query = query.strip()
    if params and isinstance(params, dict):
        prepared = prepare_for_mongo(params)
        for key, value in prepared.items():
            query = query.replace("%({0})s".format(key), value)
    if "findOne" in query:
        query = query.replace("findOne", "find_one")
    if config.echo_sql:
        logging.info(query)
    res = eval(query)
    return res


class MgSession(BaseSession):
    def __init__(self, db=None, host=None, user=None, port=None, pwd=None):
        super().__init__()
        self.db, _ = mongodb_connect(db, host, port, user, pwd)
        if self.db == "":
            raise Exception(_)
        else:
            self.client = _

    def get_db_list(self):
        return self.client.list_database_names()

    def get_table_list(self):
        return self.db.list_collection_names()

    def execute(self, sql, params=None):
        return query_params_for_mongo(self.db, sql, params)

    def collection(self, table):
        return self.db[table]

    def insert(self, table, values):
        self.collection(table).insert(values)

    def update(self, table, condition, values, upsert=False):
        self.collection(table).update(condition, {"$set": values}, upsert=upsert)

    def delete(self, table, condition):
        self.collection(table).remove(condition)

    def query(self, table, condition={}, columns=None, single=False):
        columns_dict = {}
        if columns:
            if isinstance(columns, dict):
                columns_dict.update(columns)
            elif isinstance(columns, list):
                for column_name in columns:
                    columns_dict[column_name] = 1
        else:
            columns_dict = None
        if single:
            cursor = self.collection(table).find_one(condition, columns_dict)
        else:
            cursor = self.collection(table).find(condition, columns_dict)
        return cursor

    def query_all(self, sql, params=None, data_type="dict", columns: list = None):
        res = query_params_for_mongo(self.db, sql, params)
        if data_type == "dict":
            return list(res)
        elif data_type == "list":
            result = []
            for item in res:
                result_item = []
                if not columns:
                    columns = item.keys()
                for column in columns:
                    result_item.append(item[column])
                result.append(result_item)
            return result
        else:
            return res

    def query_one(self, sql, params=None, data_type="dict", columns: list = None):
        res = query_params_for_mongo(self.db, sql, params)
        if data_type == "dict":
            return res
        elif data_type == "list":
            result = []
            if not columns:
                columns = res.keys()
            for column in columns:
                result.append(res[column])
            return result
        elif data_type == "object":
            return res.values()[0]
        else:
            return res
