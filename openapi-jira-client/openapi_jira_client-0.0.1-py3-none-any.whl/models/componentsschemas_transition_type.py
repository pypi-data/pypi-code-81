from enum import Enum


class ComponentsschemasTransitionType(str, Enum):
    GLOBAL_ = "global"
    INITIAL = "initial"
    DIRECTED = "directed"

    def __str__(self) -> str:
        return str(self.value)
