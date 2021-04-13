# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import asyncio
import typing
from collections import deque

from w8_auto_py.common.emitter import AbstractEmitterTask
from w8_auto_py.common.validator import is_async_task

ATask = asyncio.Task
ATaskDeque = typing.Deque[ATask]
ATaskIterable = typing.Iterable[ATask]
JoinReturnType = typing.TypeVar("JoinReturnType")


async def join(task: AbstractEmitterTask, **kwargs) -> typing.List[JoinReturnType]:
    if not isinstance(task, AbstractEmitterTask):
        raise TypeError("task params type error")

    done = []

    for result in asyncio.as_completed(task):
        value = await result
        done.append(value)

    return done


class EmitterQueue(AbstractEmitterTask):
    """
    使用队列实现
    """

    def __init__(self, max_len: int = None):
        self.__max_len = max_len
        self.__queue = deque(maxlen=self.max_len)

    @property
    def empty(self) -> bool:
        return self.length <= 0

    @property
    def max_len(self) -> int:
        if not isinstance(self.__max_len, int):
            self.__max_len = 2 ** 31
        return abs(self.__max_len)

    @property
    def length(self):
        return len(self.queue)

    @property
    def queue(self) -> ATaskDeque:
        return self.__queue

    def add_task(self, task: ATask, **kwargs) -> None:
        """
        添加任务
        :param task:
        :param kwargs:
        :return:
        """
        if not is_async_task(task):
            raise TypeError("task must be asyncio.Task, use asyncio.create_task()")

        self.queue.append(task)

    def __iter__(self) -> ATaskIterable:
        for _ in enumerate(range(self.length)):
            yield self.popleft()

    def popleft(self) -> ATask:
        if self.length:
            return self.queue.popleft()
