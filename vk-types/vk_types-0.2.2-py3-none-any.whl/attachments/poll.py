from ..base import BaseModel
from vk_types.attachments import Photo
from vk_types.additional import PhotoSizes

from typing import List, Optional
import typing


# https://vk.com/dev/objects/poll


class PollAnswer(BaseModel):
    id: int
    text: str
    votes: int
    rate: typing.Union[int, float]


class PollBackgroundPoint(BaseModel):
    position: typing.Union[int, float]
    color: str


class PollBackground(BaseModel):
    id: int
    type: str
    angle: int
    color: str
    width: Optional[int]
    height: Optional[int]
    images: Optional[List[PhotoSizes]]
    points: List[PollBackgroundPoint]

class PollFriends(BaseModel):
    id: int


class Poll(BaseModel):
    id: int
    owner_id: int
    created: int
    question: str
    votes: int
    answers: List[PollAnswer]
    anonymous: bool
    multiple: bool
    answer_ids: List[int]
    end_date: int
    closed: bool
    is_board: bool
    can_edit: bool
    can_vote: bool
    can_report: bool
    can_share: bool
    author_id: Optional[int]
    photo: Optional[Photo]
    background: Optional[PollBackground]
    friends: Optional[List[PollFriends]]

