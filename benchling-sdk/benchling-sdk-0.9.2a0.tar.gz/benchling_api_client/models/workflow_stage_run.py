import datetime
from typing import Any, Dict, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.workflow_stage_run_status import WorkflowStageRunStatus

T = TypeVar("T", bound="WorkflowStageRun")


@attr.s(auto_attribs=True)
class WorkflowStageRun:
    """  """

    created_at: datetime.datetime
    id: str
    name: str
    status: WorkflowStageRunStatus

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id
        name = self.name
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "createdAt": created_at,
                "id": id,
                "name": name,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("createdAt"))

        id = d.pop("id")

        name = d.pop("name")

        status = WorkflowStageRunStatus(d.pop("status"))

        workflow_stage_run = cls(
            created_at=created_at,
            id=id,
            name=name,
            status=status,
        )

        return workflow_stage_run
