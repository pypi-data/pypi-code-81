from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_create_workflow_transition_details_type import (
    ComponentsschemasCreateWorkflowTransitionDetailsType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWorkflowTransitionDetails")


@attr.s(auto_attribs=True)
class CreateWorkflowTransitionDetails:
    """ The details of a workflow transition. """

    name: str
    to: str
    type_: ComponentsschemasCreateWorkflowTransitionDetailsType
    description: Union[Unset, str] = UNSET
    from_: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        to = self.to
        type_ = self.type_.value

        description = self.description
        from_: Union[Unset, List[str]] = UNSET
        if not isinstance(self.from_, Unset):
            from_ = self.from_

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "to": to,
                "type": type_,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if from_ is not UNSET:
            field_dict["from"] = from_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        to = d.pop("to")

        type_ = ComponentsschemasCreateWorkflowTransitionDetailsType(d.pop("type"))

        description = d.pop("description", UNSET)

        from_ = cast(List[str], d.pop("from", UNSET))

        create_workflow_transition_details = cls(
            name=name,
            to=to,
            type_=type_,
            description=description,
            from_=from_,
        )

        return create_workflow_transition_details
