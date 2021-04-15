from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PublishedWorkflowId")


@attr.s(auto_attribs=True)
class PublishedWorkflowId:
    """ Properties that identify a published workflow. """

    name: str
    entity_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        entity_id = self.entity_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        entity_id = d.pop("entityId", UNSET)

        published_workflow_id = cls(
            name=name,
            entity_id=entity_id,
        )

        return published_workflow_id
