# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import asyncio
import enum
import functools

from w8_auto_py.typings import Function, KwargsType, PoolExecutorTypes
from w8_auto_py.common.runner import AbstractRunStrategy, IRunner
from w8_auto_py.common.validator import callable_validator, coroutine_func_validator
from w8_auto_py.util import EnumUtil


class CoroutineStrategy(AbstractRunStrategy):
    """
    协程对象策略
    """

    def __init__(self, runner: IRunner):
        self.__runner = runner

    @property
    def runner(self):
        return self.__runner

    async def execute(self):
        return await self.runner.coro_or_func


class CoroutineFunctionStrategy(AbstractRunStrategy):
    """
    协程函数策略
    """

    def __init__(self, runner: IRunner, kwargs: KwargsType = None):
        self.__runner = runner
        self.__kwargs = kwargs

    @property
    def runner(self) -> IRunner:
        return self.__runner

    @property
    def kwargs(self) -> KwargsType:
        return self.__kwargs

    def _is_coroutine_func(self, func: Function) -> bool:
        return coroutine_func_validator(f"{func} 不是一个协程函数").is_validate(func)

    async def _impl_execute(self, runner: IRunner, kwargs):
        """
        实现
        :param runner:
        :param kwargs:
        :return:
        """
        return await runner.coro_or_func(*runner.args, **kwargs)

    async def execute(self):
        return await self._impl_execute(self.runner,
                                        kwargs=self.kwargs)


class FunctionStrategy(AbstractRunStrategy):
    """
    普通函数策略
    """

    def __init__(self,
                 runner: IRunner,
                 executor: PoolExecutorTypes = None):
        self.__runner = runner
        self.__executor = executor

    @property
    def runner(self) -> IRunner:
        return self.__runner

    @property
    def executor(self) -> PoolExecutorTypes:
        return self.__executor

    def _is_callable(self, func: Function) -> bool:
        return callable_validator(f"{func} 不是一个可调用对象").is_validate(func)

    async def _impl_execute(self,
                            runner: IRunner,
                            executor: PoolExecutorTypes = None):
        """
        execute 实现
        :param runner
        :param executor:
        :return:
        """
        loop = asyncio.get_running_loop()
        if not loop:
            loop = asyncio.get_event_loop()

        fut = loop.run_in_executor(executor, runner.coro_or_func, *runner.args)
        return await fut

    async def execute(self):
        return await self._impl_execute(self.runner,
                                        executor=self.executor)


class RunStrategy(enum.Enum):
    COROUTINE = CoroutineStrategy
    COROUTINE_FUNCTION = CoroutineFunctionStrategy
    FUNCTION = FunctionStrategy


def create_runner_strategy(strategy: RunStrategy,
                           runner: IRunner,
                           **kwargs) -> AbstractRunStrategy:
    if not isinstance(strategy, RunStrategy):
        strategy = RunStrategy.COROUTINE_FUNCTION

    f = functools.partial(
        EnumUtil.get_enum_value(strategy),
        runner=runner
    )
    return f(**kwargs)
