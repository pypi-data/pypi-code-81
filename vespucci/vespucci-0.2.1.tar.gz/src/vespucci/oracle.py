import asyncio
import logging
from asyncio.queues import LifoQueue, Queue  # pylint: disable=ungrouped-imports
from contextlib import AsyncExitStack
from typing import AsyncGenerator, Callable, Generic, Tuple, TypeVar, MutableMapping

from vespucci.utils import Combined
from vespucci.base import Edge, Tag

log = logging.getLogger(__name__)


N = TypeVar("N")


class Oracle(Generic[N]):

    _seeds: Combined[Tag, Tuple[N, int]]
    _revealed: MutableMapping[Tag, Queue]
    _fn_calls: MutableMapping[Tag, int]

    def __init__(self, fn: Callable[[N], Edge[N]], capacity: int = 100):
        self._fn = fn
        self._capacity = capacity
        self._seeds = Combined(LifoQueue(maxsize=self._capacity))
        self._revealed = {}
        self._fn_calls = {}
        self._process_task = None
        self._merged = None

    async def enter(self, stack: AsyncExitStack):
        return await stack.enter_async_context(self)

    async def seed(self, tag: Tag, node: N, rank: int):
        await self._seeds.put_nowait(tag, (node, rank))

    async def reveal(self, tag: Tag) -> AsyncGenerator[Tuple[Edge[N], int], None]:
        while True:
            (edge, rank) = await self._revealed[tag].get()
            yield (edge, rank)

    def in_process(self, tag: Tag) -> int:
        return self._seeds.qsize(tag) + self._revealed[tag].qsize() + self._fn_calls[tag]

    def register(self, tag: Tag, capacity: int = 0) -> None:
        if tag not in self._revealed:
            self._revealed[tag] = Queue(maxsize=capacity)
            self._fn_calls[tag] = 0

    def unregister(self, tag) -> None:
        del self._fn_calls[tag]
        del self._revealed[tag]

    async def _process(self):
        while True:
            (tag, (node, rank)) = await self._seeds.get()
            # TODO: Deal with self._fn(node) raising exceptions
            self._fn_calls[tag] += 1
            edges = [e for e in await self._fn(node) if e.src != e.dst]
            if edges:
                for edge in edges:
                    await self._revealed[tag].put((edge, rank))
            else:
                # Pass control to a client waiting on a next edge to reveal
                await self._revealed[tag].put((Edge(node, None), rank))
            self._fn_calls[tag] -= 1

    async def __aenter__(self):
        self._process_task = asyncio.create_task(self._process())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self._process_task, "cancel"):
            self._process_task.cancel()
