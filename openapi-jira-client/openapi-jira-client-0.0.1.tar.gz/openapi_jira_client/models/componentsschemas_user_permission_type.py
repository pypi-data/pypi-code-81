from enum import Enum


class ComponentsschemasUserPermissionType(str, Enum):
    GLOBAL_ = "GLOBAL"
    PROJECT = "PROJECT"

    def __str__(self) -> str:
        return str(self.value)
