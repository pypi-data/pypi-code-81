from enum import Enum


class ComponentsschemasHierarchyLevelGlobalHierarchyLevel(str, Enum):
    SUBTASK = "SUBTASK"
    BASE = "BASE"
    EPIC = "EPIC"

    def __str__(self) -> str:
        return str(self.value)
