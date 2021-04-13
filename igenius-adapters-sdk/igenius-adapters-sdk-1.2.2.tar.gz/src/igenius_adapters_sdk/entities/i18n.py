from typing import NewType

from pydantic import BaseModel

LocaliseKey = NewType("LocaliseKey", str)


class I18n(BaseModel):
    name: LocaliseKey
    description: LocaliseKey
