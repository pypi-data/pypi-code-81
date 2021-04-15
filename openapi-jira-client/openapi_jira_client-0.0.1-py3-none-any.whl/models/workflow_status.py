from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.workflow_status_properties import WorkflowStatusProperties
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowStatus")


@attr.s(auto_attribs=True)
class WorkflowStatus:
    """ Details of a workflow status. """

    id_: str
    name: str
    properties: Union[Unset, WorkflowStatusProperties] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "name": name,
            }
        )
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        name = d.pop("name")

        properties: Union[Unset, WorkflowStatusProperties] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = WorkflowStatusProperties.from_dict(_properties)

        workflow_status = cls(
            id_=id_,
            name=name,
            properties=properties,
        )

        return workflow_status
