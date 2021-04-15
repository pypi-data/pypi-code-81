from enum import Enum


class ComponentsschemasFieldChangedClauseOperator(str, Enum):
    CHANGED = "changed"

    def __str__(self) -> str:
        return str(self.value)
