import datetime
from typing import Any, Dict, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="Workflow")


@attr.s(auto_attribs=True)
class Workflow:
    """  """

    created_at: datetime.datetime
    description: str
    display_id: str
    id: str
    name: str
    project_id: str

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        description = self.description
        display_id = self.display_id
        id = self.id
        name = self.name
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "createdAt": created_at,
                "description": description,
                "displayId": display_id,
                "id": id,
                "name": name,
                "projectId": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("createdAt"))

        description = d.pop("description")

        display_id = d.pop("displayId")

        id = d.pop("id")

        name = d.pop("name")

        project_id = d.pop("projectId")

        workflow = cls(
            created_at=created_at,
            description=description,
            display_id=display_id,
            id=id,
            name=name,
            project_id=project_id,
        )

        return workflow
