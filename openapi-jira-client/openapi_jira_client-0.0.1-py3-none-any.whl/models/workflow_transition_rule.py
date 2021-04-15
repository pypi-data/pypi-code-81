from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTransitionRule")


@attr.s(auto_attribs=True)
class WorkflowTransitionRule:
    """ A workflow transition rule. """

    type_: str
    configuration: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type_ = self.type_
        configuration = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type_,
            }
        )
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = d.pop("type")

        configuration = None

        workflow_transition_rule = cls(
            type_=type_,
            configuration=configuration,
        )

        return workflow_transition_rule
