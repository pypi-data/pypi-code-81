from typing import List, TypeVar, Generic
from abc import ABC, abstractmethod
from contextlib import AsyncExitStack

from vespucci.base import Edge


N = TypeVar("N")


class Store(Generic[N], ABC):
    @abstractmethod
    async def save(self, edge: Edge[N]) -> None:
        pass

    @abstractmethod
    # IMPROVE: The return type should be Optional[List[N]], with None indicating
    # that the node is not in the graph store. However, this makes implementing
    # clients more complicated. Now, returning an empty list means that `src` is
    # not in the store, thereby losing the distinction between not being in the
    # store, and having no suggestions.
    async def load(self, src: N) -> List[N]:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def enter(self, stack: AsyncExitStack):
        return await stack.enter_async_context(self)
