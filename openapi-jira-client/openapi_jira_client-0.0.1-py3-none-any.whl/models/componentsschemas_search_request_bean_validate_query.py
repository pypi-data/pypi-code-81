from enum import Enum


class ComponentsschemasSearchRequestBeanValidateQuery(str, Enum):
    STRICT = "strict"
    WARN = "warn"
    NONE = "none"
    TRUE = "true"
    FALSE = "false"

    def __str__(self) -> str:
        return str(self.value)
