from enum import Enum


class AddWorklogAdjustEstimate(str, Enum):
    NEW = "new"
    LEAVE = "leave"
    MANUAL = "manual"
    AUTO = "auto"

    def __str__(self) -> str:
        return str(self.value)
