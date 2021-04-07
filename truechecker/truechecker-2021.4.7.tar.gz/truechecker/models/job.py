from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class JobStates(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"
    ERROR = "error"


class CheckJob(BaseModel):
    id: str
    bot_id: int
    state: JobStates
    progress: float
    created: datetime
    description: Optional[str]
