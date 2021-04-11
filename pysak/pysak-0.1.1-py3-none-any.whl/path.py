import os
import sys

SakRootPath = ""


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


# 设置项目的根目录
def setRootPath(path: str):
    """
        设置项目的根目录
    @param path:
    @return:
    """
    global SakRootPath
    SakRootPath = path
    return True


# 获取项目根目录 PS：调用前需要先setRootPath
def getRootPath():
    """
        获取项目根目录
    :return:
    """
    global SakRootPath
    if SakRootPath == "":
        print("请先调用 setRootPath 设置项目根目录")
        return False
    return SakRootPath


# 检测目录/文件是否存在
def isPathExists(path=""):
    """
        检测 目录 或 文件 是否存在
    :param path: 路径
    :return:
    """
    if path == "":
        return False

    return os.path.exists(path)


# 创建目录 PS：若路径不存在，则递归创建，若存在则不执行）
def mkdir(path: str):
    """
        递归创建目录
        1、若路径不存在，则递归创建。
        2、若路径已存在，则不执行。
    :param path: 路径
    :return:
    """
    if not isPathExists(path):
        os.makedirs(path)
        return True
    else:
        return False
