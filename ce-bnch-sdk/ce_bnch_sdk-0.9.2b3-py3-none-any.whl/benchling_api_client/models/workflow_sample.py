import datetime
from typing import Any, cast, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="WorkflowSample")


@attr.s(auto_attribs=True)
class WorkflowSample:
    """  """

    batch_id: str
    container_ids: List[str]
    created_at: datetime.datetime
    id: str
    name: str

    def to_dict(self) -> Dict[str, Any]:
        batch_id = self.batch_id
        container_ids = self.container_ids

        created_at = self.created_at.isoformat()

        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "batchId": batch_id,
                "containerIds": container_ids,
                "createdAt": created_at,
                "id": id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_id = d.pop("batchId")

        container_ids = cast(List[str], d.pop("containerIds"))

        created_at = isoparse(d.pop("createdAt"))

        id = d.pop("id")

        name = d.pop("name")

        workflow_sample = cls(
            batch_id=batch_id,
            container_ids=container_ids,
            created_at=created_at,
            id=id,
            name=name,
        )

        return workflow_sample
