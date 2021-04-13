# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import abc
import typing

from w8_auto_py.typings import NumberTypes

T = typing.TypeVar("T")


class AbstractQpsTimer(metaclass=abc.ABCMeta):
    """
    抽象计时器
    """

    @property
    def is_timeout(self) -> bool:
        """
        是否超时
        Returns:

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_current(self) -> NumberTypes:
        """
        获取当前时间
        Returns:

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def set_timeout(self) -> T:
        """
        设置超时
        Returns:

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def clear(self) -> T:
        """
        清除超时
        Returns:

        """
        raise NotImplementedError()


class AbstractQpsCounter(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def count(self) -> NumberTypes:
        raise NotImplementedError()

    @abc.abstractmethod
    def increment(self, num: NumberTypes) -> T:
        """
        增加计数
        Args:
            num:

        Returns:

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def clear(self) -> T:
        """
        清零
        Returns:

        """
        raise NotImplementedError()


class AbstractQueryPerSecond(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def start(self) -> None:
        """
        开始
        Returns:

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def clear(self) -> T:
        """
        清零
        Returns:

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def auto_increment(self) -> T:
        """
        自增
        Returns:

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> T:
        raise NotImplementedError()
