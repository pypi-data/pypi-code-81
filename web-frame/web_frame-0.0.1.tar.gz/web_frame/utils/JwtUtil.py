import logging
import time

import jwt
from jwt import DecodeError

from web_frame.context import config
from web_frame.utils.CommonUtil import sys_date_format, check_expire
from web_frame.utils.MysqlUtil import SqlSession

JWT_PASSWORD = "gis-server-123"


def generate_session(key):
    headers = {
        'alg': "HS256",
    }
    jwt_token = jwt.encode({"from": key},
                           JWT_PASSWORD,  # key
                           algorithm="HS256",
                           headers=headers
                           ).decode('ascii')
    return jwt_token


def generate_token(user_info):
    # payload
    key = user_info["username"]
    token_dict = {
        "create_time": sys_date_format(),  # 时间戳
        "key": key,  # self-defined
        "iat": time.time(),  # fixed
    }
    # headers
    headers = {
        'alg': "HS256",
    }
    jwt_token = jwt.encode(token_dict,
                           JWT_PASSWORD,  # key
                           algorithm="HS256",
                           headers=headers
                           ).decode('ascii')

    logging.debug("generate jwt:{}".format(jwt_token))
    return jwt_token


# 获取user_info
def generate_token_info(token):
    user_info = {}
    try:
        user_info = jwt.decode(token, JWT_PASSWORD)
    except DecodeError:
        logging.debug("generate jwt failed:{}".format(token))
    logging.debug("generate jwt:{}".format(user_info["key"]))
    return user_info


def auth(token, username=None):
    user_name = ""
    logging.warning("get token in auth:<{}>".format(token))
    if not username or not token or str(token) == "null":
        return False
    try:
        payload = jwt.decode(token,
                             JWT_PASSWORD,
                             leeway=7 * 24 * 3600,
                             options={"verify_exp": True}
                             )
        user_name = payload.get("key", "")
        create_time = payload.get("create_time", "")
        # 过期校验
        if check_expire(create_time, 7):
            logging.warning("auth failed, token expired with payload user_name:{}".format(user_name))
            return False
        # 验证cookie 中的username
        if user_name != username:
            logging.debug("auth failed, illegal username:{} with payload user_name:{}".format(username, user_name))
            return False
        # 验证数据库
        if len(config.user_table) > 0:
            user_info = SqlSession().query_one(
                "SELECT * FROM {} WHERE username = '{}'".format(config.user_table, user_name))
            if not user_info:
                return False
        return True
    except jwt.ExpiredSignatureError as e:
        logging.debug("auth failed")
    except jwt.exceptions.InvalidSignatureError as e:
        logging.debug("auth failed")
    logging.warning("auth failed, with payload user_name:{}".format(user_name))
    return False
