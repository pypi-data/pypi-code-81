# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import asyncio
from collections.abc import Callable


def is_function(value) -> bool:
    return isinstance(value, Callable)


def is_coroutine(value) -> bool:
    return asyncio.iscoroutine(value)


def is_coroutine_function(value) -> bool:
    return asyncio.iscoroutinefunction(value)


def is_async_task(task) -> bool:
    return isinstance(task, asyncio.Task)
