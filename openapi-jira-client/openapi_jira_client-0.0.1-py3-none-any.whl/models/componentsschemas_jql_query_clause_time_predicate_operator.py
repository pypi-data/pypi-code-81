from enum import Enum


class ComponentsschemasJqlQueryClauseTimePredicateOperator(str, Enum):
    BEFORE = "before"
    AFTER = "after"
    FROM_ = "from"
    TO = "to"
    ON = "on"
    DURING = "during"
    BY = "by"

    def __str__(self) -> str:
        return str(self.value)
