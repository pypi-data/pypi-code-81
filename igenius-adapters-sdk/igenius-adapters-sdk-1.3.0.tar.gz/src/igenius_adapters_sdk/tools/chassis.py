from typing import Callable, List, Mapping

from pydantic import BaseModel

from igenius_adapters_sdk.entities import query
from igenius_adapters_sdk.tools import utils


class Chassis(BaseModel):
    query: query.Query
    engine: Callable

    async def async_run(self) -> List[Mapping]:
        result = await self.engine(self.query)
        if hasattr(self.query, "bin_interpolation") and self.query.bin_interpolation:
            result = utils.bin_interpolation(self.query, result)
        return result

    def run(self) -> List[Mapping]:
        result = self.engine(self.query)
        if hasattr(self.query, "bin_interpolation") and self.query.bin_interpolation:
            result = utils.bin_interpolation(self.query, result)
        return result
