from enum import Enum


class ComponentsschemasJsonNodeNumberType(str, Enum):
    INT = "INT"
    LONG = "LONG"
    BIG_INTEGER = "BIG_INTEGER"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    BIG_DECIMAL = "BIG_DECIMAL"

    def __str__(self) -> str:
        return str(self.value)
