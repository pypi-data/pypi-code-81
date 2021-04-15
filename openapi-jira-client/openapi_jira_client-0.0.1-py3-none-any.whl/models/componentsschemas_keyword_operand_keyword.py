from enum import Enum


class ComponentsschemasKeywordOperandKeyword(str, Enum):
    EMPTY = "empty"

    def __str__(self) -> str:
        return str(self.value)
