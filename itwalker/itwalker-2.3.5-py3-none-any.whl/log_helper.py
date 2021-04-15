import os
import stat
import datetime
import json
from enum import Enum


class LOG_LEVEL(Enum):
    """
    日志级别
    """
    debug = 3
    info = 2
    warning = 1
    error = 0


class LOG_COLOR(Enum):
    """
    日志颜色
    """
    debug = "32m"
    info = "36m"
    warning = "33m"
    error = "31m"


is_init = False


def default_log(msg):
    pass


class LogHandler():
    def __init__(self, log_color, base_folder):
        if not isinstance(log_color, LOG_COLOR):
            raise Exception("log_color must be LOG_COLOR class!")
        self.log_color = log_color
        self.base_folder = base_folder

    def base_log(self, msg):
        if isinstance(msg, str):
            pass
        if isinstance(msg, Exception):
            if msg.__getattribute__("args"):
                if isinstance(msg.args, tuple) or isinstance(msg.args, list):
                    msg = '-'.join([str(v) for v in msg.args])
        msg = f"{self.log_color.name} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {json.dumps(msg, ensure_ascii=False)}"
        print(f"\033[{self.log_color.value}", msg, "\033[0m")
        with open(
                os.path.join(self.base_folder, self.log_color.name,
                             datetime.datetime.today().strftime('%Y-%m-%d') + '.log'),
                mode="a+", encoding='utf-8') as f:
            f.writelines(msg + "\n")


class LogHelper:
    def init_folder(self):
        global is_init
        if not is_init:
            for folder in self.folder_list:
                filepath = os.path.join(self.base_folder, folder)
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                    os.chmod(filepath, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            is_init = True
        for v in list(LOG_LEVEL):
            if v.name in self.folder_list:
                color = LOG_COLOR.__members__.get(v.name)
                self.__setattr__(v.name, LogHandler(color, self.base_folder).base_log)
            else:
                self.__setattr__(v.name, default_log)

    def __init__(self, log_level=LOG_LEVEL.debug):
        if not isinstance(log_level, LOG_LEVEL):
            raise Exception("log_level must be LOG_LEVEL class!")
        self.base_folder = os.path.join(os.getcwd(), 'static', 'logs')
        self.folder_list = [v.name for v in list(LOG_LEVEL) if log_level.value >= v.value]
        self.init_folder()

    def base_log(self, log_color, msg):
        if log_color.name not in self.folder_list:
            return
        if isinstance(msg, str):
            pass
        if isinstance(msg, Exception):
            if msg.__getattribute__("args"):
                if isinstance(msg.args, tuple) or isinstance(msg.args, list):
                    msg = '-'.join([str(v) for v in msg.args])
        msg = f"{log_color.name} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {json.dumps(msg, ensure_ascii=False)}"
        print(f"\033[{log_color.value}", msg, "\033[0m")
        with open(
                os.path.join(self.base_folder, log_color.name, datetime.datetime.today().strftime('%Y-%m-%d') + '.log'),
                mode="a+", encoding='utf-8') as f:
            f.writelines(msg + "\n")
