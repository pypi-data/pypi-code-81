# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import functools

from w8_auto_py.common.validator import AbstractValidator
from w8_auto_py.common.validator import (
    CallableValidator,
    CoroutineValidator,
    CoroutineFunctionValidator
)


def validator_factory(validator: AbstractValidator,
                      error_message: str,
                      **kwargs) -> AbstractValidator:
    """
    校验器工厂
    :param validator:
    :param error_message:
    :param kwargs:
    :return:
    """
    if not issubclass(validator, AbstractValidator):
        raise TypeError("validator 必须是 AbstractValidator 子类")
    f = functools.partial(validator, error_message=error_message)
    return f(**kwargs)


def callable_validator(error_message: str) -> CallableValidator:
    return validator_factory(CallableValidator, error_message)


def coroutine_validator(error_message: str) -> CoroutineValidator:
    return validator_factory(CoroutineValidator, error_message)


def coroutine_func_validator(error_message: str) -> CoroutineFunctionValidator:
    return validator_factory(CoroutineFunctionValidator, error_message)
