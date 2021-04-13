# @Time     : 2021/3/28
# @Project  : w8_auto_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import asyncio
import enum
import functools

from w8_auto_py.typings import ArgsType, KwargsType, PoolExecutorTypes
from w8_auto_py.util import EnumUtil
from w8_auto_py.common.emitter import AbstractEmitterStrategy, IEmitter, join


class CoroutineEmitterStrategy(AbstractEmitterStrategy):
    """
    协程函数策略
    """

    def __init__(self,
                 emitter: IEmitter,
                 args: ArgsType = None,
                 kwargs: KwargsType = None):
        self.__emitter = emitter
        self.__args = () if not args else args
        self.__kwargs = {} if not kwargs else kwargs

    @property
    def emitter(self) -> IEmitter:
        return self.__emitter

    @property
    def args(self) -> ArgsType:
        return self.__args

    @property
    def kwargs(self) -> KwargsType:
        return self.__kwargs

    async def _impl_run(self, emitter: IEmitter, args: ArgsType, kwargs: KwargsType):
        for _ in enumerate(range(emitter.max_len)):
            t = asyncio.create_task(
                emitter.coro_or_func(*args, **kwargs)
            )
            emitter.task.add_task(t)
            await asyncio.sleep(emitter.delay)

        return await join(emitter.task)

    async def run(self):
        return await self._impl_run(self.emitter, self.args, self.kwargs)


class FunctionEmitterStrategy(AbstractEmitterStrategy):
    """
    普通函数策略
    """

    def __init__(self,
                 emitter: IEmitter,
                 args: ArgsType = None,
                 executor: PoolExecutorTypes = None):
        self.__emitter = emitter
        self.__args = () if not args else args
        self.__executor = executor

    @property
    def emitter(self) -> IEmitter:
        return self.__emitter

    @property
    def args(self) -> ArgsType:
        return self.__args

    @property
    def executor(self) -> PoolExecutorTypes:
        return self.__executor

    async def _create_async_func(self,
                                 executor: PoolExecutorTypes,
                                 emitter: IEmitter,
                                 args: ArgsType):
        loop = asyncio.get_running_loop()
        if not loop:
            loop = asyncio.get_event_loop()

        return await loop.run_in_executor(executor, emitter.coro_or_func, *args)

    async def _impl_run(self,
                        executor: PoolExecutorTypes,
                        emitter: IEmitter,
                        args: ArgsType):

        for _ in enumerate(range(emitter.max_len)):
            t = asyncio.create_task(
                self._create_async_func(executor, emitter, args)
            )
            emitter.task.add_task(t)
            await asyncio.sleep(emitter.delay)

        return await join(emitter.task)

    async def run(self):
        return await self._impl_run(self.executor, self.emitter, self.args)


class EmitterStrategy(enum.Enum):
    COROUTINE = CoroutineEmitterStrategy
    FUNCTION = FunctionEmitterStrategy


def create_emitter_strategy(strategy: EmitterStrategy,
                            emitter: IEmitter,
                            **kwargs) -> AbstractEmitterStrategy:
    klass = EnumUtil.get_enum_value(strategy)
    f = functools.partial(klass, emitter=emitter)
    return f(**kwargs)
