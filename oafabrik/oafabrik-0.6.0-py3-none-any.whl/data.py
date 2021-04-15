from abc import abstractmethod, ABC

import pandas as pd
import pydantic

from pyfabrik.models import (
    FabrikRawReadResponse,
    FabrikException,
    FabrikRawWriteProfileResponse,
)


class DataFrameFacade(ABC):
    @abstractmethod
    def read_data_frame(self, r: FabrikRawReadResponse) -> pd.DataFrame:
        pass

    @abstractmethod
    def write_data_frame(
        self, df: pd.DataFrame, profile: FabrikRawWriteProfileResponse
    ):
        pass


class DefaultDataFrameFacade(DataFrameFacade):
    class ParquetContext(pydantic.BaseModel):
        landing_zone_kind: str
        path: str

    def write_data_frame(
        self, df: pd.DataFrame, profile: FabrikRawWriteProfileResponse
    ):
        fmt = profile.context.get("format")

        if fmt == "parquet":
            return DefaultDataFrameFacade.write_parquet(df, profile.context.get("path"))

        raise FabrikException(f"Unsupported format `{fmt}`.")

    def read_data_frame(self, r: FabrikRawReadResponse) -> pd.DataFrame:
        if r.format.lower() == "parquet":
            return DefaultDataFrameFacade.read_parquet(r)

        raise FabrikException(f"Unsupported format `{r.format}`.")

    @staticmethod
    def write_parquet(df: pd.DataFrame, dest: str, **kwargs):
        return df.to_parquet(dest + "results.parquet.snappy", **kwargs)

    @staticmethod
    def read_parquet(r: FabrikRawReadResponse) -> pd.DataFrame:
        ctx = DefaultDataFrameFacade.ParquetContext.parse_obj(r.context)
        return pd.read_parquet(ctx.path)
