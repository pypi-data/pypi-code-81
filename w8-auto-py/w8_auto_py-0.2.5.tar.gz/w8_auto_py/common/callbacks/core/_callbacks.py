# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from w8_auto_py.typings import Function
from w8_auto_py.common.callbacks import AbstractCallback, filter_function, filter_async_function
from w8_auto_py.common.validator import callable_validator, coroutine_func_validator


class Callback(AbstractCallback):

    def __init__(self, *callbacks):
        super().__init__(*filter_function(*callbacks))

    def add(self, callback: Function) -> None:
        callable_validator(
            error_message=f"{callback} 需要一个函数或对象"
        ).is_validate(callback)

        self.set.add(callback)

    def extend(self, *callbacks) -> None:
        return self.set.update(filter_function(*callbacks))


class ACallback(AbstractCallback):

    def __init__(self, *acallbacks):
        super().__init__(*filter_async_function(*acallbacks))

    def add(self, callback: Function) -> None:
        coroutine_func_validator(
            error_message=f"{callback} 需要一个协程函数"
        ).is_validate(callback)

        self.set.add(callback)

    def extend(self, *callbacks) -> None:
        return self.set.update(filter_async_function(*callbacks))
