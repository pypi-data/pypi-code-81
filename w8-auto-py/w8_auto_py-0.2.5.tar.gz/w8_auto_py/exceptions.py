# @Time     : 2021/3/26
# @Project  : w8_auto_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
class ValidateException(Exception):
    pass


class NotCoroutineError(ValidateException):
    pass


class NotCoroutineFunctionError(ValidateException):
    pass


class NotCallableError(ValidateException):
    pass
