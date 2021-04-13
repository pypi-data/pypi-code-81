from collections import Counter
import asyncio
from asyncio import Queue, create_task
from typing import Mapping, Hashable, TypeVar, Generic, Tuple, MutableMapping
from vespucci.base import Tag


class _Merged(Queue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tasks = []

    def stop(self):
        for task in self._tasks:
            task.cancel()

    def count(self, tag: Tag) -> int:
        pass


K = TypeVar("K", bound=Hashable)
T = TypeVar("T")


class Combined(Generic[K, T]):
    _qsize: MutableMapping[K, int]

    def __init__(self, queue: Queue):
        self._queue = queue
        self._qsize = Counter()

    async def get(self) -> Tuple[K, T]:
        (key, item) = await self._queue.get()
        self._qsize[key] -= 1
        if self._qsize[key] == 0:
            del self._qsize[key]
        return (key, item)

    async def put(self, key: K, item: T):
        self._qsize[key] += 1
        return self._queue.put((key, item))

    async def put_nowait(self, key: K, item: T):
        self._qsize[key] += 1
        return self._queue.put_nowait((key, item))

    def qsize(self, key: K) -> int:
        return self._qsize[key]


async def merge(inqs: Mapping[Hashable, Queue], **kwargs) -> Queue:
    async def move(tag, inq, outq):
        try:
            while True:
                item = await inq.get()
                await outq.put((tag, item))
        except asyncio.CancelledError:
            return

    outq = _Merged(**kwargs)

    for (tag, inq) in inqs.items():
        # pylint: disable=protected-access
        outq._tasks.append(create_task(move(tag, inq, outq)))

    return outq
