from abc import abstractmethod, ABC

import pandas as pd
import pydantic

from pyfabrik.models import FabrikRawReadResponse, FabrikException


class DataFrameFacade(ABC):
    @abstractmethod
    def read_data_frame(self, r: FabrikRawReadResponse) -> pd.DataFrame:
        pass


class DefaultDataFrameFacade(DataFrameFacade):
    class ParquetContext(pydantic.BaseModel):
        landing_zone_kind: str
        path: str

    def read_data_frame(self, r: FabrikRawReadResponse) -> pd.DataFrame:
        if r.format == "PARQUET":
            return DefaultDataFrameFacade.read_parquet(r)

        raise FabrikException(f"Unsupported format `{r.format}`.")

    @staticmethod
    def read_parquet(r: FabrikRawReadResponse) -> pd.DataFrame:
        ctx = DefaultDataFrameFacade.ParquetContext.parse_obj(r.context)
        return pd.read_parquet(ctx.path)
