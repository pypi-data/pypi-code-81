from enum import Enum


class ComponentsschemasProjectForScopeProjectTypeKey(str, Enum):
    SOFTWARE = "software"
    SERVICE_DESK = "service_desk"
    BUSINESS = "business"

    def __str__(self) -> str:
        return str(self.value)
