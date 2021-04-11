r"""
pysak is a simple, powerful and clean python common function library.

Github Repository: https://github.com/1Gbps/pysak
"""

SakUserPlatform = None


# 检查 python 版本
def checkPythonVersion():
    import platform

    pythonVersion = platform.python_version()
    pythonVersion = pythonVersion.split(".")

    MajorVersionNumber = int(pythonVersion[0])  # 主版本号
    MinorVersionNumber = int(pythonVersion[1])  # 子版本号
    RevisionNumber = int(pythonVersion[2])  # 修正版本号

    if MajorVersionNumber < 3:
        print("Sak 暂不兼容 python 3 以下的版本")
        exit()


# 获取 Platform 信息
def getUserPlatform():
    import platform

    global SakUserPlatform
    SakUserPlatform = platform.uname()

    return True


checkPythonVersion()
getUserPlatform()

from .basic import *
from .config import *
from .debug import *
from .file import *
from .img import *
from .MyThread import *
from .path import *
from .time import *
from .user_agent import *
