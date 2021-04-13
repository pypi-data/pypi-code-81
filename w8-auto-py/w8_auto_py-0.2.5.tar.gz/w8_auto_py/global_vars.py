# @Time     : 2021/3/26
# @Project  : w8_auto_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import enum

_G_BASE_NUMBER = 10
G_ENCODING: str = "utf-8"


class TimeUnit(enum.Enum):
    """
    时间单位
    """
    S = _G_BASE_NUMBER ** 0  # 秒
    MS = _G_BASE_NUMBER ** -3  # 毫秒
    US = _G_BASE_NUMBER ** -6  # 微秒


class NumberUnit(enum.Enum):
    """
    数学单位
    """
    B = _G_BASE_NUMBER ** 2  # 百
    Q = _G_BASE_NUMBER ** 3  # 千
    M = _G_BASE_NUMBER ** 6  # 兆
