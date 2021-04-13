# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import abc
from w8_auto_py.typings import Function, FunctionIterable, FunctionSet


class AbstractCallback(metaclass=abc.ABCMeta):

    def __init__(self, *callbacks):
        self._set: FunctionSet = set(callbacks)

    @property
    def set(self) -> FunctionSet:
        return self._set

    @property
    def empty(self) -> bool:
        return not self.length

    @property
    def length(self) -> int:
        return len(self.set)

    def remove(self, callback: Function) -> None:
        if self.empty:
            return None

        return self.set.remove(callback)

    def __iter__(self) -> FunctionIterable:
        if not self.empty:
            for callback in self.set:
                yield callback

    @abc.abstractmethod
    def add(self, callback: Function) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def extend(self, *callbacks) -> None:
        raise NotImplementedError()
