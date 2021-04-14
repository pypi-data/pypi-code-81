from typing import Optional

from pydantic import BaseModel


class Url(BaseModel):
    url: str


class AuthorizationResponse(BaseModel):
    state: str
    code: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
