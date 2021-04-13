# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import abc
import typing

from w8_auto_py.typings import ArgsType, Interface

T = typing.TypeVar("T")
RunnerReturnType = typing.TypeVar("RunnerReturnType")


class AbstractRunner(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def coro_or_func(self) -> T:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def args(self) -> ArgsType:
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self) -> RunnerReturnType:
        raise NotImplementedError("NotImplementedError .run()")


class AbstractRunStrategy(metaclass=abc.ABCMeta):
    """
    策略接口
    """

    @property
    @abc.abstractmethod
    def runner(self):
        raise NotImplementedError("NotImplementedError .execute()")

    @abc.abstractmethod
    async def execute(self) -> RunnerReturnType:
        raise NotImplementedError("NotImplementedError .execute()")


class IRunner(Interface):
    """
    runner 接口
    """

    @property
    def coro_or_func(self) -> T:
        raise NotImplementedError()

    @property
    def args(self) -> ArgsType:
        raise NotImplementedError()

    def run(self) -> T:
        raise NotImplementedError()


class IRunStrategy(Interface):
    """
    RunStrategy 接口
    """

    @property
    def runner(self) -> IRunner:
        raise NotImplementedError()

    async def execute(self) -> RunnerReturnType:
        raise NotImplementedError()
