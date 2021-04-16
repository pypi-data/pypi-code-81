from pydantic import BaseModel


class BaseModelName(BaseModel):
    object: str = None

    def __init__(self, **data):
        data["object"] = self.__class__.__name__
        super().__init__(**data)
