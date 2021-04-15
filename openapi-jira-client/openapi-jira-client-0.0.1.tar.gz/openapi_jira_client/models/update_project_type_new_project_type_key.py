from enum import Enum


class UpdateProjectTypeNewProjectTypeKey(str, Enum):
    SOFTWARE = "software"
    SERVICE_DESK = "service_desk"
    BUSINESS = "business"

    def __str__(self) -> str:
        return str(self.value)
