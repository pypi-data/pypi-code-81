# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from w8_auto_py.typings import (
    ArgsType,
    Function,
    KwargsType,
    NumberTypes,
    PoolExecutorTypes
)
from w8_auto_py.global_vars import TimeUnit
from w8_auto_py.common.emitter import create_emitter_strategy, delay, AbstractEmitter, IEmitterTask, EmitterStrategy
from w8_auto_py.common.validator import is_function, is_coroutine_function


class Emitter(AbstractEmitter):
    """
    并发器
    """

    def __init__(self,
                 coro_or_func: Function,
                 task: IEmitterTask,
                 max_len: int,
                 delay: NumberTypes = 500,
                 time_unit: TimeUnit = TimeUnit.MS,
                 args: ArgsType = None,
                 executor: PoolExecutorTypes = None,
                 kwargs: KwargsType = None):
        """
        并发器对象
        :param coro_or_func:
        :param task:
        :param max_len:
        :param delay:
        :param time_unit:
        :param args:
        :param executor:
        :param kwargs:
        """
        self.__coro_or_func = coro_or_func
        self.__task = task
        self.__args = () if not isinstance(args, tuple) else args
        self.__kwargs = {} if not isinstance(kwargs, dict) else kwargs
        self.__executor = executor

        """ 辅助变量 """
        self.__delay = delay
        self.__max_len = max_len
        self.__time_unit = time_unit
        self.__cache_delay: NumberTypes = 0

    @property
    def coro_or_func(self) -> Function:
        return self.__coro_or_func

    @property
    def delay(self) -> NumberTypes:
        if not self.__cache_delay:
            self.__cache_delay = delay(self.__delay, self.__time_unit)
        return self.__cache_delay

    @property
    def max_len(self) -> int:
        """
        控制最大并发数量
        :return:
        """
        if not isinstance(self.__max_len, int):
            return 2 ** 31
        return abs(self.__max_len)

    @property
    def task(self) -> IEmitterTask:
        return self.__task

    @property
    def args(self) -> ArgsType:
        return self.__args

    @property
    def kwargs(self) -> KwargsType:
        return self.__kwargs

    @property
    def executor(self):
        return self.__executor

    async def _impl_run(self):
        if is_coroutine_function(self.coro_or_func):
            """ 协程函数策略 """
            strategy = create_emitter_strategy(
                EmitterStrategy.COROUTINE,
                self, args=self.args, kwargs=self.kwargs
            )
            return await strategy.run()

        elif is_function(self.coro_or_func):
            """ 普通函数策略 """
            strategy = create_emitter_strategy(
                EmitterStrategy.FUNCTION,
                self, args=self.args, executor=self.executor
            )
            return await strategy.run()

        else:
            raise ValueError("coro_or_func 参数需要一个协程函数或普通函数")

    async def run(self):
        return await self._impl_run()

    def __str__(self):
        return f"{self.__coro_or_func.__name__} + {self.delay}"
