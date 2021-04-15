from enum import Enum


class ComponentsschemasUserAccountType(str, Enum):
    ATLASSIAN = "atlassian"
    APP = "app"
    CUSTOMER = "customer"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
