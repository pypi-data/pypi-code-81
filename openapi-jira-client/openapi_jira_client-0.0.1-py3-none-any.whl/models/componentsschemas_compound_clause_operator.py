from enum import Enum


class ComponentsschemasCompoundClauseOperator(str, Enum):
    AND_ = "and"
    OR_ = "or"
    NOT_ = "not"

    def __str__(self) -> str:
        return str(self.value)
