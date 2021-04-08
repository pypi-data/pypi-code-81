import pysak
import time


def getTimestamp(length=10):
    """
        获取当前时刻指定长度的时间戳  10位~17位
    :param length:
    :return:
    """

    if length > 17 or length < 10:
        return False

    # 计算差值
    cha = length - 10
    timestamp = pysak.time()

    if cha == 0:
        timestamp = int(timestamp)
    elif cha > 0:
        timestamp = int(timestamp * pow(10, cha))

    return timestamp


def getDate():
    ltime = time.localtime(getTimestamp(10))
    return time.strftime("%Y-%m-%d %H:%M:%S", ltime)
