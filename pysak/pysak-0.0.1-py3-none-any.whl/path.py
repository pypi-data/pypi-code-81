import os
import sys


def getPath(config_name=""):
    """获取路径 返回运行本函数的文件绝对路径+config_name
    determine if application is a script file or frozen exe
    """
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    config_path = os.path.join(application_path, config_name)
    return config_path


# 获取项目根目录
def getRootPath():
    """
        获取项目根目录
    :return:
    """
    return getPath("..\\")


def mkdir(path: str):
    """
        目录
        若目录不存在，则递归创建
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)

    return True


def isPathExists(path: str):
    """
        检测目录/文件是否存在
    :param path:
    :return:
    """
    return os.path.exists(path)
