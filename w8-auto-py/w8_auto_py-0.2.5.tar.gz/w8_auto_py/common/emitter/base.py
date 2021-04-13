# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import abc
import typing
from collections.abc import Awaitable

from w8_auto_py.typings import Function, Interface, NumberTypes
from w8_auto_py.global_vars import TimeUnit

T = typing.TypeVar("T")
EmitterReturnType = typing.TypeVar("EmitterReturnType")
EmitterMasterReturnType = typing.TypeVar("EmitterMasterReturnType")


def delay(delay: NumberTypes, time_unit: TimeUnit = TimeUnit.MS) -> NumberTypes:
    if not isinstance(delay, int):
        delay = 1

    if not isinstance(time_unit, TimeUnit):
        time_unit = TimeUnit.MS

    return delay * time_unit.value


class AbstractEmitterTask(metaclass=abc.ABCMeta):
    """
    抽象并发器任务
    """

    @abc.abstractmethod
    def add_task(self, task: T, **kwargs) -> None:
        """
        添加
        :param task:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def length(self) -> int:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def empty(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def __iter__(self) -> typing.Iterable[T]:
        raise NotImplementedError()


class AbstractEmitter(Awaitable, metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def coro_or_func(self) -> Function:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def delay(self) -> NumberTypes:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def max_len(self) -> int:
        raise NotImplementedError()

    @property
    def task(self) -> AbstractEmitterTask:
        raise NotImplementedError()

    @abc.abstractmethod
    async def run(self, *args, **kwargs) -> T:
        raise NotImplementedError()

    async def start(self) -> T:
        return await self.run()

    def __await__(self):
        return self.start().__await__()


class AbstractEmitterMaster(Awaitable, metaclass=abc.ABCMeta):
    """
    抽象并发管理组
    """

    def __init__(self,
                 task: AbstractEmitterTask,
                 delay: NumberTypes,
                 time_unit: TimeUnit = TimeUnit.MS):
        self.__task = task
        self.__delay = delay
        self.__time_unit = time_unit

        self.__cache_delay: NumberTypes = 0

    @property
    def delay(self) -> NumberTypes:
        if not self.__cache_delay:
            self.__cache_delay = delay(self.__delay, self.__time_unit)
        return self.__cache_delay

    @property
    def task(self) -> AbstractEmitterTask:
        return self.__task

    @abc.abstractmethod
    def add(self, emitter: AbstractEmitter, **kwargs) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def extends(self, *emitters, **kwargs) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def run(self, *args, **kwargs) -> EmitterMasterReturnType:
        raise NotImplementedError()

    async def start(self, *args, **kwargs) -> EmitterMasterReturnType:
        return await self.run(*args, **kwargs)

    def __await__(self):
        return self.start().__await__()


class AbstractEmitterStrategy(metaclass=abc.ABCMeta):
    """
    抽象并发策略
    """

    @property
    @abc.abstractmethod
    def emitter(self) -> AbstractEmitter:
        raise NotImplementedError()

    @abc.abstractmethod
    async def run(self, *args, **kwargs) -> EmitterReturnType:
        raise NotImplementedError()


class IEmitterTask(Interface):
    """
    并发任务接口
    """

    def add_task(self, task: T, **kwargs) -> None:
        raise NotImplementedError()

    def __iter__(self) -> typing.Iterable[T]:
        raise NotImplementedError()


class IEmitter(Interface):
    """
    并发器接口
    """

    @property
    def coro_or_func(self) -> Function:
        raise NotImplementedError()

    @property
    def delay(self) -> NumberTypes:
        raise NotImplementedError()

    @property
    def max_len(self) -> int:
        raise NotImplementedError()

    @property
    def task(self) -> IEmitterTask:
        raise NotImplementedError()

    async def start(self) -> EmitterReturnType:
        raise NotImplementedError()


class IEmitterMaster(Interface):

    @abc.abstractmethod
    def add(self, emitter: AbstractEmitter, **kwargs) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def extends(self, *emitters, **kwargs) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def start(self) -> EmitterMasterReturnType:
        raise NotImplementedError()

    @abc.abstractmethod
    async def join(self) -> EmitterMasterReturnType:
        raise NotImplementedError()
