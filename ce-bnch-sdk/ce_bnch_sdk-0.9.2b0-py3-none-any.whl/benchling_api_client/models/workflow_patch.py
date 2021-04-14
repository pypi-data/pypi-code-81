from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowPatch")


@attr.s(auto_attribs=True)
class WorkflowPatch:
    """  """

    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        name = self.name
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if project_id is not UNSET:
            field_dict["projectId"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        project_id = d.pop("projectId", UNSET)

        workflow_patch = cls(
            description=description,
            name=name,
            project_id=project_id,
        )

        return workflow_patch
