import datetime
import inspect
import json
import logging
import random
import socket
import time
from decimal import Decimal

from bson import ObjectId


def generate_random_key(code_len=6):
    all_char = '0123456789qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJIKOLP'
    index = len(all_char) - 1
    code = ''
    for _ in range(code_len):
        num = random.randint(0, index)
        code += all_char[num]
    return code


def sys_date_format(dt=datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S", type="datetime", delta=0):
    if delta == 0:
        sys_date = dt.strftime(format)
    else:
        sys_date = (dt - datetime.timedelta(delta)).strftime(format)
    if type == "datetime":
        return sys_date
    elif type == "date":
        return sys_date.split(" ")[0]
    elif type == "time":
        return sys_date.split(" ")[-1]


def calculate_date(start, end):
    return (end - start).days


# 校验是否过期，true已过期，false未过期
def check_expire(start, limit):
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    val = calculate_date(start_date, datetime.datetime.now())
    return val >= limit


def split_comma_str(item):
    if not item or len(item.strip()) == 0:
        return []
    else:
        return str(item).split(",")


def split_comma_int(item):
    res = []
    if not item or len(item.strip()) == 0:
        return res
    for v in item.split(","):
        if "-" in v:
            [start, stop] = v.split("-")
            for i in range(int(start), int(stop) + 1):
                res.append(i)
        elif ":" in v:
            [start, step, stop] = v.split(":")
            if len(step) == 0:
                step = '1'
            for i in range(int(start), int(stop) + 1, int(step)):
                res.append(i)
        else:
            res.append(int(v))
    return res


def is_not_empty(obj):
    if not obj or len(str(obj).strip()) == 0:
        return False
    return True


def is_empty(obj):
    if not obj or len(str(obj).strip()) == 0:
        return True
    return False


def check_empty(*obj):
    for item in obj:
        if is_empty(item):
            raise Exception("缺少必要的参数: {}".format(obj.__name__))


def validate_date(date):
    try:
        date_str = str(date)
        if ":" in date_str:
            if len(date_str) < 19:
                time.strptime(date_str, "%Y-%m-%d %H:%M")
            else:
                time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# 用于判断一个字符串是否符合Json格式
def check_json_format(raw_msg):
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.timedelta):
            return str(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


# 获取方法参数默认值
def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


# 获取方法参数类型
def get_annotation_args(func):
    signature = inspect.signature(func)
    return {
        k: v.annotation
        for k, v in signature.parameters.items()
    }


def get_func_params(func):
    func_params = func.__code__.co_varnames
    if func_params and len(func_params) > 1:
        return func_params[1:func.__code__.co_argcount]
    else:
        logging.warning(f"方法：{func.__name__}未获取到参数！")
        return []


# 解析param
def parse_val(val, val_type):
    new_val = val
    if isinstance(val, bytes) or isinstance(val, bytearray):
        new_val = val.decode("utf-8")
    if isinstance(val, list):
        val_list = []
        for item in val:
            val_item = parse_val(item, None)
            val_list.append(val_item)
        if val_type == list:
            return val_list
        else:
            new_val = val_list
    if type(new_val) != val_type:
        if val_type == int:
            return int(new_val)
        elif val_type == str and isinstance(new_val, list):
            return new_val[0]
        else:
            return new_val
    return new_val


# 解析command
def get_command(self, func_name):
    command = ""
    params = None
    is_json = False
    if "get" in func_name:
        command = self.get_argument("command", "")
    elif "post" in func_name:
        params_str = ""
        if not self.request.files and len(self.request.body.decode('utf8')) > 0:
            params_str = self.request.body.decode('utf8')
            is_json = check_json_format(params_str)
        if is_json:
            params = json.loads(params_str)
            command = params.get("command", "")
        else:
            params = self.request.arguments
            command = self.get_argument("command", "")
            command = parse_val(command, str)
    return command, params, is_json
