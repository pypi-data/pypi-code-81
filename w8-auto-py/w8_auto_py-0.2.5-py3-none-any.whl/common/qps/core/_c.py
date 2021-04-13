# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from w8_auto_py.typings import NumberTypes
from w8_auto_py.common.qps import AbstractQpsCounter


class QpsCounter(AbstractQpsCounter):

    def __init__(self, count: NumberTypes):
        self.__count = int(count)

    @property
    def count(self) -> NumberTypes:
        return self.__count

    def increment(self, num: NumberTypes) -> None:
        if not isinstance(num, (int, float)):
            raise TypeError("num must be int or float")
        self.__count += num

    def clear(self) -> None:
        self.__count = 0
