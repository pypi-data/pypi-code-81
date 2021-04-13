# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import asyncio

from w8_auto_py.typings import ArgsType, Function, KwargsType, PoolExecutorTypes
from w8_auto_py import NotCallableError
from w8_auto_py.common.validator import callable_validator
from w8_auto_py.common.runner import AbstractRunner
from w8_auto_py.common.runner import create_runner_strategy, RunStrategy


class AsyncRunner(AbstractRunner):

    def __init__(self,
                 coro_or_func: Function,
                 args: ArgsType = None,
                 kwargs: KwargsType = None,
                 executor: PoolExecutorTypes = None):
        """

        Args:
            coro_or_func:   函数、协程函数、协程对象
            args:           函数或协程函数 位置参数
            kwargs:         函数或协程函数 关键字参数
            executor:       普通函数的执行器，默认线程，支持进程
        """

        self.__coro_or_func = coro_or_func
        self.__args = args
        self.__kwargs = kwargs
        self.__executor = executor

    @property
    def coro_or_func(self) -> Function:
        return self.__coro_or_func

    @property
    def args(self) -> ArgsType:
        if not isinstance(self.__args, tuple):
            self.__args = ()
        return self.__args

    @property
    def kwargs(self) -> KwargsType:
        if not isinstance(self.__kwargs, dict):
            self.__kwargs = {}
        return self.__kwargs

    @property
    def executor(self) -> PoolExecutorTypes:
        return self.__executor

    def set_loop_policy(self, loop_policy=None):
        if not loop_policy:
            return
        asyncio.set_event_loop_policy(loop_policy)

    def _is_callable(self, func: Function) -> bool:
        try:
            return callable_validator(f"{func} 需要一个函数或对象").is_validate(func)
        except NotCallableError:
            return False

    def _is_coroutine_function(self, func: Function) -> bool:
        return asyncio.iscoroutinefunction(func)

    def _is_coroutine(self, func: Function) -> bool:
        return asyncio.iscoroutine(func)

    async def _function_strategy(self, runner, executor: PoolExecutorTypes = None):
        """
        普通函数执行策略
        Args:
            runner:
            executor:

        Returns:

        """
        strategy = create_runner_strategy(
            strategy=RunStrategy.FUNCTION,
            runner=runner,
            executor=executor
        )
        return await strategy.execute()

    async def _coro_function_strategy(self, runner, kwargs):
        """
        协程函数执行策略
        Args:
            runner:
            kwargs:

        Returns:

        """

        strategy = create_runner_strategy(
            strategy=RunStrategy.COROUTINE_FUNCTION,
            runner=runner, kwargs=kwargs
        )
        return await strategy.execute()

    async def _coro_strategy(self, runner):
        """
        协程对象策略
        Args:
            runner:

        Returns:

        """

        strategy = create_runner_strategy(
            strategy=RunStrategy.COROUTINE,
            runner=runner
        )

        return await strategy.execute()

    async def _impl_run(self, runner):

        if self._is_coroutine(runner.coro_or_func):
            # print("coroutine strategy ...")
            return await self._coro_strategy(runner)

        elif self._is_coroutine_function(runner.coro_or_func):
            # print("coroutine function strategy ...")
            return await self._coro_function_strategy(runner, runner.kwargs)

        elif self._is_callable(runner.coro_or_func):
            # print("function strategy ...")
            return await self._function_strategy(runner, runner.executor)

        else:
            # print("not support strategy ...")
            raise ValueError("coro_or_func 参数非法")

    def run(self):
        return asyncio.run(self._impl_run(self))
