from dataclasses import dataclass
from typing import Generic, TypeVar, Hashable


N = TypeVar("N")


@dataclass(frozen=True, eq=True)
class Edge(Generic[N]):
    src: N
    dst: N


Tag = Hashable


def arc_fn(neighbor_fn):
    async def fn(node):
        nodes = await neighbor_fn(node)
        return [Edge(src=node, dst=n) for n in nodes]

    return fn
