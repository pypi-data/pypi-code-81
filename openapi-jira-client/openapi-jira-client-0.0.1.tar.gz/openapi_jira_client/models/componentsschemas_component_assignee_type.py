from enum import Enum


class ComponentsschemasComponentAssigneeType(str, Enum):
    PROJECT_DEFAULT = "PROJECT_DEFAULT"
    COMPONENT_LEAD = "COMPONENT_LEAD"
    PROJECT_LEAD = "PROJECT_LEAD"
    UNASSIGNED = "UNASSIGNED"

    def __str__(self) -> str:
        return str(self.value)
