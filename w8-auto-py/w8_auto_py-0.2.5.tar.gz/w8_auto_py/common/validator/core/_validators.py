# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import typing

from w8_auto_py.typings import Function
from w8_auto_py import (
    NotCallableError,
    NotCoroutineError,
    NotCoroutineFunctionError
)
from w8_auto_py.common.validator import AbstractValidator
from w8_auto_py.common.validator import is_function, is_coroutine, is_coroutine_function


class CallableValidator(AbstractValidator):

    def is_validate(self, value: Function) -> bool:
        if not is_function(value):
            raise NotCallableError(f"{self.error_message}, {value}")
        return True


class CoroutineValidator(AbstractValidator):

    def is_validate(self, value: typing.Coroutine) -> bool:
        if not is_coroutine(value):
            raise NotCoroutineError(f"{self.error_message}, {value}")
        return True


class CoroutineFunctionValidator(AbstractValidator):

    def is_validate(self, value: Function) -> bool:
        if not is_coroutine_function(value):
            raise NotCoroutineFunctionError(f"{self.error_message}, {value}")
        return True
