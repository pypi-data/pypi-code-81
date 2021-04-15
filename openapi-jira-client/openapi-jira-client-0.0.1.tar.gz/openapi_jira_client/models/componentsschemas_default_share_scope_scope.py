from enum import Enum


class ComponentsschemasDefaultShareScopeScope(str, Enum):
    GLOBAL_ = "GLOBAL"
    AUTHENTICATED = "AUTHENTICATED"
    PRIVATE = "PRIVATE"

    def __str__(self) -> str:
        return str(self.value)
