from enum import Enum


class ComponentsschemasFieldWasClauseOperator(str, Enum):
    WAS = "was"
    WAS_IN = "was in"
    WAS_NOT_IN = "was not in"
    WAS_NOT = "was not"

    def __str__(self) -> str:
        return str(self.value)
