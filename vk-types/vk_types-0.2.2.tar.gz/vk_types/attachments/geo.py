from typing import Optional

from ..base import BaseModel
from ..additional import Place


class Geo(BaseModel):
    type: str
    coordinates: str
    place: Optional[Place]
