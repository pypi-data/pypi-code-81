import json
import redis
import logging

from web_frame.context import config
from web_frame.utils.CommonUtil import CJsonEncoder


def get_conn(host=None, port=None):
    if not host:
        host = config.cache_ip
    if not port:
        port = config.cache_port
    redis_conn = redis.Redis(host=host, port=port)
    return redis_conn


def get_cache(key):
    try:
        value = get_conn().get(key)
    except ConnectionError as e:
        logging.warning(f"缓存服务连接失败：{e}")
        value = None
    if value:
        result = value.decode()
        logging.debug("hit cache: {}".format(key))
        return json.loads(result)
    logging.debug("miss cache: {}".format(key))
    return None


def set_cache(key, value):
    logging.debug(f"set cache: {key}")
    try:
        get_conn().set(key, json.dumps(value, cls=CJsonEncoder, ensure_ascii=False))
    except ConnectionError as e:
        logging.warning(f"缓存服务连接失败：{e}")
