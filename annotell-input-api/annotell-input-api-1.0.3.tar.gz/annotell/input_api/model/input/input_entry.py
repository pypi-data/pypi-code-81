from dataclasses import dataclass
from typing import Optional
from enum import Enum
from annotell.input_api.model.abstract.abstract_models import Response


class InputStatus(str, Enum):
    Processing = "processing"
    Created = "created"
    Failed = "failed"
    InvalidatedBadContent = "invalidated:broken-input"
    InvalidatedSlamRerun = "invalidated:slam-rerun"
    InvalidatedDuplicate = "invalidated:duplicate"
    InvalidatedIncorrectlyCreated = "invalidated:incorrectly-created"


@dataclass
class Input(Response):
    uuid: str
    external_id: str
    batch: str
    input_type: str
    status: InputStatus
    error_message: Optional[str]

    @staticmethod
    def from_json(js: dict):
        return Input(
            js["internalId"],
            js["externalId"],
            js["batchId"],
            js["inputType"],
            js["status"],
            js.get("errorMessage")
        )
