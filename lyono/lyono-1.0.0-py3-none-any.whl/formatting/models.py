import abc
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Union

from lyono import BaseModel
from lyono.typings import DictAny, StdTypes

from .enums import CRUD


class Payload(BaseModel):
    bucket: str
    event_at: datetime = datetime.now()
    tags: DictAny = {}
    data: DictAny = {}
    namespace: DictAny = {}


class Command(BaseModel):
    command: CRUD = CRUD.POST
    payload: Union[Payload, DictAny] = {}


if __name__ == "__main__":
    cmd = Command()
    send_cmd = cmd.dict()
