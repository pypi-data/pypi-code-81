__version__ = "0.1.0"
from dataclasses import InitVar, dataclass
from enum import Enum
from typing import TYPE_CHECKING

import orjson

# Here we implement the dataclasses so we can get type completion thru the entire project.
from pydantic import BaseModel as PydanticBaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


from .formatting.models import Command

if TYPE_CHECKING:
    from typing import Any, Deque, Dict, List, Optional, TypedDict, Union

    # from pydantic import BaseModel

    StdTypes = Union[bool, int, float, str, dict]
    DictAny = Dict[str, Any]

else:
    from pydantic.dataclasses import dataclass
