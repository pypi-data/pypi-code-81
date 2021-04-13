from datetime import datetime
from typing import List, Optional, Any
from pathlib import Path

from pydantic import BaseModel, EmailStr

from .util import GeoLocation



#############################################
class Acervo(BaseModel):
    titulo: str
    autor: str
    media_type: str
    description: str = ''
    tags: List[str] = []
    thumbnail: Optional[bytes] = None
    licence: Optional[str] = None
#############################################
