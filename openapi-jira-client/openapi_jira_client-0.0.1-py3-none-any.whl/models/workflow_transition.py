from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkflowTransition")


@attr.s(auto_attribs=True)
class WorkflowTransition:
    """ A workflow transition. """

    id_: int
    name: str

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        name = d.pop("name")

        workflow_transition = cls(
            id_=id_,
            name=name,
        )

        return workflow_transition
