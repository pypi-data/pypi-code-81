# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import enum
import functools

from w8_auto_py.typings import ArgsType, Function, KwargsType, NumberTypes, PoolExecutorTypes
from w8_auto_py.global_vars import TimeUnit
from w8_auto_py.common.emitter import (
    AbstractEmitter,
    Emitter,
    EmitterCollection,
    EmitterGroup,
    EmitterReturnType,
    EmitterQueue
)
from w8_auto_py.common.runner import create_arunner, run
from w8_auto_py.util import EnumUtil


class Emitters(enum.Enum):
    EMITTER = Emitter
    EMITTER_GROUP = EmitterGroup
    EMITTER_COLLECTION = EmitterCollection


class EmitterFactory:

    @classmethod
    def create_task(cls, max_len: int) -> EmitterQueue:
        return EmitterQueue(max_len=max_len)

    @classmethod
    def _factory(cls,
                 emitters: Emitters,
                 delay: NumberTypes = 500,
                 time_unit: TimeUnit = TimeUnit.MS,
                 **kwargs) -> AbstractEmitter:
        klass = EnumUtil.get_enum_value(emitters)
        f = functools.partial(
            klass,
            delay=delay,
            time_unit=time_unit
        )
        return f(**kwargs)

    @classmethod
    def create(cls,
               emitters: Emitters,
               task: EmitterQueue,
               delay: NumberTypes = 500,
               time_unit: TimeUnit = TimeUnit.MS,
               **kwargs) -> AbstractEmitter:
        return cls._factory(
            emitters=emitters,
            task=task,
            delay=delay,
            time_unit=time_unit,
            **kwargs
        )


def create_emitter(coro_or_func: Function,
                   args: ArgsType = None,
                   kwargs: KwargsType = None,
                   executor: PoolExecutorTypes = None,
                   delay: NumberTypes = 500,
                   max_len: int = None,
                   time_unit: TimeUnit = TimeUnit.MS) -> Emitter:
    """
    创建并发器
    :param coro_or_func:
    :param args:
    :param kwargs:
    :param executor:
    :param delay:
    :param max_len:
    :param time_unit:
    :return:
    """

    task = EmitterFactory.create_task(max_len)
    return EmitterFactory.create(
        emitters=Emitters.EMITTER,
        coro_or_func=coro_or_func,
        task=task,
        delay=delay,
        max_len=max_len,
        time_unit=time_unit,
        args=args,
        kwargs=kwargs,
        executor=executor
    )


def emitter_decorator(max_len: int = None,
                      delay: NumberTypes = 500,
                      time_unit: TimeUnit = TimeUnit.MS,
                      executor: PoolExecutorTypes = None) -> Emitter:
    """
    并发包装器
    :param max_len:
    :param delay:
    :param time_unit:
    :param executor:
    :return:
    """

    def _decorate(coro_or_func: Function):
        @functools.wraps(coro_or_func)
        def _wrapper(*args, **kwargs) -> Emitter:
            return create_emitter(
                coro_or_func=coro_or_func,
                delay=delay,
                max_len=max_len,
                time_unit=time_unit,
                args=args,
                kwargs=kwargs,
                executor=executor
            )

        return _wrapper

    return _decorate


def create_emitter_group(max_len: int = None,
                         delay: NumberTypes = 500,
                         time_unit: TimeUnit = TimeUnit.MS) -> EmitterGroup:
    """
    创建 并发组
    Args:
        max_len:
        delay:
        time_unit:

    Returns:

    """
    task = EmitterFactory.create_task(max_len)
    return EmitterFactory.create(
        emitters=Emitters.EMITTER_GROUP,
        task=task,
        delay=delay,
        time_unit=time_unit
    )


def create_emitter_collection(max_Len: int = None,
                              delay: NumberTypes = 500,
                              time_unit: TimeUnit = TimeUnit.MS) -> EmitterCollection:
    """
    创建 并发集合
    Args:
        max_Len:
        delay:
        time_unit:

    Returns:

    """
    task = EmitterFactory.create_task(max_Len)
    return EmitterFactory.create(
        emitters=Emitters.EMITTER_COLLECTION,
        task=task,
        delay=delay,
        time_unit=time_unit
    )


def start(emitter: AbstractEmitter, loop_policy=None) -> EmitterReturnType:
    """
    运行并发器
    Args:
        emitter:
        loop_policy:
    Returns:

    """
    runner = create_arunner(emitter.start())
    runner.set_loop_policy(loop_policy)
    return run(runner)
