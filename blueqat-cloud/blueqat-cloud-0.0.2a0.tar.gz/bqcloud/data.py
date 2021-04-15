"""Data classes and enums for communications."""
from dataclasses import dataclass
from enum import Enum
from json import JSONEncoder
from typing import Optional, SupportsIndex


@dataclass
class ExecutionRequest:
    """Internal data of task to be executed."""
    action: str
    device: str
    device_parameters: str
    shots: int
    task_group: Optional[str]
    send_email: bool


class ExecutionRequestEncoder(JSONEncoder):
    """JSONEncoder for ExecutionRequest"""
    def default(self, o):
        if isinstance(o, ExecutionRequest):
            return {
                'action': o.action,
                'device': o.device,
                'deviceParameters': o.device_parameters,
                'shots': o.shots,
                'taskGroup': o.task_group,
                'sendEmail': o.send_email
            }
        return super().default(o)


@dataclass
class TaskData:
    """Internal data of task object."""
    id: str
    userId: str
    action: str
    device: str
    deviceParameters: str
    shots: int
    createdAt: str
    updatedAt: str
    version: str


@dataclass
class TaskListData:
    """List of tasks which returns from API"""
    tasks: list[TaskData]
    count: int


class Status(str, Enum):
    """Statuses"""
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLING = "CANCELLED"
    CANCELLED = "CANCELLED"

    def is_done(self) -> bool:
        """Check whether the status is finished (completed, failed or cancelled) or not"""
        return self in (Status.COMPLETED, Status.FAILED, Status.CANCELLED)
