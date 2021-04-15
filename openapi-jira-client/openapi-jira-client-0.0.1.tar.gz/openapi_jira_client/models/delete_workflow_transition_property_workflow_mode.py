from enum import Enum


class DeleteWorkflowTransitionPropertyWorkflowMode(str, Enum):
    LIVE = "live"
    DRAFT = "draft"

    def __str__(self) -> str:
        return str(self.value)
