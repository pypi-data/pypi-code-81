# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import abc


class AbstractValidator(metaclass=abc.ABCMeta):
    """
    抽象校验器
    """

    def __init__(self, error_message: str):
        self._error_message = error_message

    @property
    def error_message(self) -> str:
        if self._error_message is None:
            return ""
        return self._error_message

    @abc.abstractmethod
    def is_validate(self, value) -> bool:
        """
        校验方法
        :param value:
        :return:
        """
        raise NotImplementedError("NotImplementedError .is_validate(value)")

    def __call__(self, value, **kwargs) -> bool:
        return self.is_validate(value)
