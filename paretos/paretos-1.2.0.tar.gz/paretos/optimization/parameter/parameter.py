from typing import Optional
from uuid import uuid4


class Parameter:
    """
    Parent class for all parameter classes‚
    """

    def __init__(self, name: str, uuid: Optional[str] = None):
        self.__name = name
        self.__uuid = uuid or str(uuid4())

    def get_id(self) -> str:
        return self.__uuid

    def get_name(self) -> str:
        return self.__name
