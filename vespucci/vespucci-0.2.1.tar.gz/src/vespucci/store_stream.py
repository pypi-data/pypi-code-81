from concurrent.futures import Executor
from typing import List, TextIO, TypeVar, Mapping, Any, Iterator, Callable
import csv
import asyncio

from vespucci.base import Edge
from vespucci.store import Store


N = TypeVar("N")

Record = Mapping[str, Any]


class StoreStream(Store[N]):
    def __init__(
        self,
        executor: Executor,
        stream: TextIO,
        records: Callable[[Edge[N]], Iterator[Record]],
    ):
        self._executor = executor
        self._stream = stream
        self._records = records
        self._writer = None

    async def save(self, edge: Edge[N]) -> None:
        def write(record):
            if self._writer is None:
                self._writer = csv.DictWriter(self._stream, fieldnames=record.keys())
                self._writer.writeheader()
            self._writer.writerow(record)
            self._stream.flush()

        for record in self._records(edge):
            await asyncio.get_running_loop().run_in_executor(self._executor, write, record)

    async def load(self, src: N) -> List[N]:
        return []
