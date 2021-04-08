import socket
import string
import uuid

from loguru import logger

UUID_CHARS = string.ascii_letters + string.digits


def get_short_id():
    uuid_str = str(uuid.uuid1()).replace('-', '')
    result = ''
    for i in range(0, 8):
        sub = uuid_str[i * 4: i * 4 + 4]
        x = int(sub, 16)
        result += UUID_CHARS[x % 0x3E]
    return result


def get_uid3():
    host_name = socket.getfqdn(socket.gethostname())
    host_ip = socket.gethostbyname(host_name)
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, __file__ + '@' + host_ip))


def log_config(msg, config):
    logger.info(msg)
    for section in config.sections():
        for k, v in config.items(section):
            logger.info('{}.{}:{}', section, k, v)
