# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from w8_auto_py.typings import FunctionIterable
from w8_auto_py.common.validator import is_function, is_coroutine_function


def filter_function(*functions) -> FunctionIterable:
    """
    过滤函数
    :param functions:
    :return:
    """
    return (
        func for func in functions if is_function(func)
    )


def filter_async_function(*afunctions) -> FunctionIterable:
    """
    过滤异步函数
    :param afunctions:
    :return:
    """
    return (
        afunc for afunc in afunctions if is_coroutine_function(afunc)
    )
