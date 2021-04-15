from enum import Enum


class UpdateWorkflowTransitionPropertyWorkflowMode(str, Enum):
    LIVE = "live"
    DRAFT = "draft"

    def __str__(self) -> str:
        return str(self.value)
