from datetime import datetime

from pydantic import BaseModel

from .users import Users


class Profile(BaseModel):
    username: str
    full_name: str
    updated: datetime
    users: Users
