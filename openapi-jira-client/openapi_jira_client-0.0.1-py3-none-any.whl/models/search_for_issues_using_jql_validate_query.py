from enum import Enum


class SearchForIssuesUsingJqlValidateQuery(str, Enum):
    STRICT = "strict"
    WARN = "warn"
    NONE = "none"
    TRUE = "true"
    FALSE = "false"

    def __str__(self) -> str:
        return str(self.value)
