import abc
from datetime import datetime
from enum import Enum
from typing import Any, Deque, Dict, List, Optional, TypedDict, Union

import orjson
from pydantic import BaseModel

StdTypes = Union[bool, int, float, str, dict]
DictAny = Dict[str, Any]
