from typing import Any

import pydantic
import pandas as pd

from pydantic import typing


class FabrikException(RuntimeError):
    pass


class FabrikReadRequest(pydantic.BaseModel):
    definition: str
    warehouse: str
    dialect: str = "dotted"
    format: str = "parquet"


class FabrikReadResponse(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    df: pd.DataFrame


class FabrikWriteRequest(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    df: pd.DataFrame
    path: str
    mode: str = "auto"


class FabrikWriteResponse(pydantic.BaseModel):
    pass


class FabrikRawReadResponse(pydantic.BaseModel):
    format: str
    context: typing.Dict[Any, Any]
