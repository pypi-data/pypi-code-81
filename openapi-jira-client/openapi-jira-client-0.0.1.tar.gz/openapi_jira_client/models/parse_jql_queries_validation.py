from enum import Enum


class ParseJqlQueriesValidation(str, Enum):
    STRICT = "strict"
    WARN = "warn"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
