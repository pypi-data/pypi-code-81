from enum import Enum


class CreateWorkflowTransitionPropertyWorkflowMode(str, Enum):
    LIVE = "live"
    DRAFT = "draft"

    def __str__(self) -> str:
        return str(self.value)
