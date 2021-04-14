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
    warehouse: str
    mode: str = "auto"


class FabrikRawWriteRequest(pydantic.BaseModel):
    path: str
    warehouse: str
    format: str = "parquet"
    context: typing.Dict[str, str] = None


class FabrikWriteResponse(pydantic.BaseModel):
    reference: str


class FabrikRawReadResponse(pydantic.BaseModel):
    format: str
    context: typing.Dict[Any, Any]


class FabrikRawWriteResponse(pydantic.BaseModel):
    reference: str


class FabrikRawWriteProfileRequest(pydantic.BaseModel):
    reference: str


class FabrikRawWriteProfileResponse(pydantic.BaseModel):
    kind: str
    context: typing.Dict[Any, Any]
