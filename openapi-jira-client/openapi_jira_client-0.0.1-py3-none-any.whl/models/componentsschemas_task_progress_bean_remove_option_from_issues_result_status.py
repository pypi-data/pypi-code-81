from enum import Enum


class ComponentsschemasTaskProgressBeanRemoveOptionFromIssuesResultStatus(str, Enum):
    ENQUEUED = "ENQUEUED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    CANCEL_REQUESTED = "CANCEL_REQUESTED"
    CANCELLED = "CANCELLED"
    DEAD = "DEAD"

    def __str__(self) -> str:
        return str(self.value)
