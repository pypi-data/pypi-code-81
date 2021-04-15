from enum import Enum


class ComponentsschemasGroupLabelType(str, Enum):
    ADMIN = "ADMIN"
    SINGLE = "SINGLE"
    MULTIPLE = "MULTIPLE"

    def __str__(self) -> str:
        return str(self.value)
