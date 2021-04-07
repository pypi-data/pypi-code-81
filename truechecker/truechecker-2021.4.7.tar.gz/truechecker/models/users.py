from pydantic import BaseModel


class Users(BaseModel):
    active: int
    stopped: int
    deleted: int
    not_found: int
