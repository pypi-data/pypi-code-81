import abc
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, validator

from igenius_adapters_sdk.entities import attribute, numeric_binning, uri

__all__ = [
    "AggregationAttribute",
    "BinningAttribute",
    "ProjectionAttribute",
]


class OrderByDirection(str, Enum):
    DESC = "desc"
    ASC = "asc"


class StaticValueAttribute(BaseModel):
    value: str
    alias: str
    default_bin_interpolation: Optional[Any]


class BaseAttribute(BaseModel, abc.ABC):
    attribute_uri: uri.AttributeUri
    alias: str


class ProjectionAttribute(BaseAttribute):
    pass


class OrderByAttribute(BaseModel):
    alias: str
    direction: OrderByDirection = OrderByDirection.ASC


class FunctionUri(BaseModel):
    function_type: Literal["group_by", "aggregation"]
    function_uid: str
    function_params: Optional[numeric_binning.BinningRules]

    @validator("function_uid")
    def check_uid_existence(cls, v, values):
        if "function_type" in values:
            if values["function_type"] == "group_by":
                attribute.GroupByFunction.from_uid(v)
            if values["function_type"] == "aggregation":
                attribute.AggregationFunction.from_uid(v)
        return v

    @validator("function_params")
    def check_binning_rules_consistency(cls, v, values):
        if v and values["function_uid"] == attribute.GroupByFunction.NUMERIC_BINNING.uid:
            if not isinstance(v, numeric_binning.BinningRules):
                raise ValueError("function_params does not contain BinningRules")
        return v


class AggregationAttribute(BaseAttribute):
    function_uri: FunctionUri
    default_bin_interpolation: Optional[Any]

    @validator("function_uri")
    def check_type(cls, v):
        if v and v.function_type and v.function_type != "aggregation":
            raise ValueError("Function type should be aggregation")
        return v


class BinningAttribute(BaseAttribute):
    function_uri: FunctionUri

    @validator("function_uri")
    def check_type(cls, v):
        if v and v.function_type and v.function_type != "group_by":
            raise ValueError("Function type should be group_by")
        return v
