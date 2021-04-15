from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkflowId")


@attr.s(auto_attribs=True)
class WorkflowId:
    """ Properties that identify a workflow. """

    name: str
    draft: bool

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        draft = self.draft

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "draft": draft,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        draft = d.pop("draft")

        workflow_id = cls(
            name=name,
            draft=draft,
        )

        return workflow_id
