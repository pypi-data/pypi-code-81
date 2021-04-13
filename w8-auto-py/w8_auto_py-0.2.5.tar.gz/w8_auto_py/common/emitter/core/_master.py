# @Time     : 2021/3/28
# @Project  : w8_auto_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import asyncio
import typing

from w8_auto_py.global_vars import TimeUnit
from w8_auto_py.typings import NumberTypes
from w8_auto_py.common.emitter import AbstractEmitterMaster, AbstractEmitter, IEmitterTask, join


class EmitterGroup(AbstractEmitterMaster):
    """
    并发组
    """

    def __init__(self,
                 task: IEmitterTask,
                 delay: NumberTypes,
                 time_unit: TimeUnit = TimeUnit.MS):
        """
        并发组管理器
        :param task:
        :param delay:
        :param time_unit:
        """
        super().__init__(task, delay, time_unit)
        self.__emitters: typing.List[AbstractEmitter] = []

    @property
    def empty(self) -> bool:
        return not self.length

    @property
    def emitters(self) -> typing.List[AbstractEmitter]:
        return self.__emitters

    @property
    def length(self) -> int:
        return len(self.emitters)

    def add(self, emitter: AbstractEmitter, **kwargs) -> None:
        """
        单个添加并发器
        Args:
            emitter:

        Returns:

        """
        if not self._is_emitter(emitter):
            raise TypeError("emitter 必须是一个并发对象")
        self.emitters.append(emitter)

    def extends(self, *emitters) -> None:
        """
        批量添加并发器
        Args:
            *emitters:

        Returns:

        """
        if not emitters:
            return

        self.emitters.extend((emitter for emitter in emitters if self._is_emitter(emitter)))

    async def run(self):
        for emitter in self:
            self.task.add_task(asyncio.create_task(emitter.start()))
            await asyncio.sleep(self.delay)

        await join(self.task)

    def _is_emitter(self, emitter) -> bool:
        return isinstance(emitter, AbstractEmitter)

    def __iter__(self) -> typing.Iterable[AbstractEmitter]:
        for _, item in enumerate(range(self.length)):
            """ 为空, 自动退出 """
            yield self._pop_head()

    def _pop_head(self) -> AbstractEmitter:
        return self.emitters.pop(0)


class EmitterCollection(AbstractEmitterMaster):
    """
    并发集合
    """

    def __init__(self,
                 task: IEmitterTask,
                 delay: NumberTypes = 500,
                 time_unit: TimeUnit = TimeUnit.MS):
        """
        并发集合管理器
        :param task:
        :param delay:
        :param time_unit:
        """
        super().__init__(task, 2 ** 0, time_unit)
        self.__emitters: typing.Set[typing.Union[AbstractEmitter,
                                                 EmitterGroup]] = set()

    @property
    def length(self) -> int:
        return len(self.emitters)

    @property
    def emitters(self) -> typing.Set[typing.Union[AbstractEmitter,
                                                  EmitterGroup]]:
        return self.__emitters

    def add(self, emitter: typing.Union[AbstractEmitter,
                                        EmitterGroup], **kwargs) -> None:
        """
        单个添加
        Args:
            emitter:

        Returns:

        """
        if not self._is_emitter(emitter):
            raise TypeError("emitter 必须是并发对象或并发组")

        self.emitters.add(emitter)

    def extends(self, *emitters) -> None:
        """
        批量添加并发器、并发组
        Args:
            *emitters:

        Returns:

        """
        self.emitters.update({emitter for emitter in emitters if self._is_emitter(emitter)})

    async def run(self):
        for emitter in self:
            self.task.add_task(asyncio.create_task(emitter.start()))
            await asyncio.sleep(self.delay)

        await join(self.task)

    def _is_emitter(self, emitter: typing.Union[AbstractEmitter,
                                                EmitterGroup]) -> bool:
        return isinstance(emitter, (AbstractEmitter, EmitterGroup))

    def __iter__(self) -> typing.Iterable[typing.Union[AbstractEmitter,
                                                       EmitterGroup]]:
        for _ in enumerate(range(self.length)):
            """ 为空, 自动退出 """
            yield self.emitters.pop()
