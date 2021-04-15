from ..base import BaseModel


class Like(BaseModel):
    count: int
    user_likes: int
    can_like: int
    can_publish: int
