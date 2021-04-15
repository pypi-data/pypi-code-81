from enum import Enum


class ComponentsschemasScopeType(str, Enum):
    PROJECT = "PROJECT"
    TEMPLATE = "TEMPLATE"

    def __str__(self) -> str:
        return str(self.value)
