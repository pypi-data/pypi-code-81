from enum import Enum


class ComponentsschemasVersionMoveBeanPosition(str, Enum):
    EARLIER = "Earlier"
    LATER = "Later"
    FIRST = "First"
    LAST = "Last"

    def __str__(self) -> str:
        return str(self.value)
