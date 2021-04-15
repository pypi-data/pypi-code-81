from enum import Enum


class DeleteWorklogAdjustEstimate(str, Enum):
    NEW = "new"
    LEAVE = "leave"
    MANUAL = "manual"
    AUTO = "auto"

    def __str__(self) -> str:
        return str(self.value)
