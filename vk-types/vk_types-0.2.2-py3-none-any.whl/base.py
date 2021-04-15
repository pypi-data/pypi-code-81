import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        allow_mutation = False

    def __str__(self):
        return str(self.dict())

    def __repr__(self):
        return f"{self.__class__} {getattr(self, 'id', getattr(self, 'type', ''))}"
