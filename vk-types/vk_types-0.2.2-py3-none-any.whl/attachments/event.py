from enum import IntEnum
from typing import List

from vk_types.base import BaseModel


class MemberStatus(IntEnum):
    coming = 1
    maybe_coming = 2
    not_coming = 3


class Event(BaseModel):
    id: int
    time: int
    member_status: MemberStatus
    is_favorite: bool
    address: str
    text: str
    button_text: str
    friends: List[int]
