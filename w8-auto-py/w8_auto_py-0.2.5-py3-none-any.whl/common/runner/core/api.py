# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import functools

from w8_auto_py.typings import ArgsType, Function, KwargsType, PoolExecutorTypes
from w8_auto_py.common.runner import AbstractRunner, AsyncRunner


def runner_factory(runner: AbstractRunner,
                   coro_or_func: Function,
                   args: ArgsType, **kwargs) -> AbstractRunner:
    if not issubclass(runner, AbstractRunner):
        raise TypeError("runner 必须是 AbstractRunner 子类")

    f = functools.partial(runner, coro_or_func=coro_or_func, args=args)

    return f(**kwargs)


def create_arunner(coro_or_func: Function,
                   args: ArgsType = None,
                   kwargs: KwargsType = None,
                   executor: PoolExecutorTypes = None) -> AsyncRunner:
    """
    异步 runner 工厂函数
    :param coro_or_func:
    :param args:
    :param kwargs:
    :param executor:
    :return:
    """
    return runner_factory(
        AsyncRunner,
        coro_or_func=coro_or_func,
        args=args,
        kwargs=kwargs,
        executor=executor
    )


def run(runner: AbstractRunner):
    return runner.run()
