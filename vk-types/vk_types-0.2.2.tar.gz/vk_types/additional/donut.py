from enum import Enum
from ..base import BaseModel


class EditMode(Enum):
    all = 'all'
    duration = 'duration'


class Donut(BaseModel):
    is_donut: bool
    paid_duration: int
    placeholder: str
    can_publish_free_copy: bool
    edit_mode: EditMode  # todo bad?
