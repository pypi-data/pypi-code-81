from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.issue_transition import IssueTransition
from ..types import UNSET, Unset

T = TypeVar("T", bound="Transitions")


@attr.s(auto_attribs=True)
class Transitions:
    """ List of issue transitions. """

    expand: Union[Unset, str] = UNSET
    transitions: Union[Unset, List[IssueTransition]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        transitions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.transitions, Unset):
            transitions = []
            for transitions_item_data in self.transitions:
                transitions_item = transitions_item_data.to_dict()

                transitions.append(transitions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if transitions is not UNSET:
            field_dict["transitions"] = transitions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        transitions = []
        _transitions = d.pop("transitions", UNSET)
        for transitions_item_data in _transitions or []:
            transitions_item = IssueTransition.from_dict(transitions_item_data)

            transitions.append(transitions_item)

        transitions = cls(
            expand=expand,
            transitions=transitions,
        )

        return transitions
