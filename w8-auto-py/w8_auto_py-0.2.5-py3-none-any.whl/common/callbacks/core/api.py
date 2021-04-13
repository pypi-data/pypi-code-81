# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import functools

from w8_auto_py.common.callbacks import AbstractCallback, Callback, ACallback


def callback_factory(callback: AbstractCallback, *functions) -> AbstractCallback:
    if not issubclass(callback, AbstractCallback):
        raise TypeError("callback 必须是 AbstractCallback 子类")

    f = functools.partial(callback)
    return f(*functions)


def callback(*functions) -> Callback:
    return callback_factory(Callback, *functions)


def acallback(*afunctions) -> ACallback:
    return callback_factory(ACallback, *afunctions)
