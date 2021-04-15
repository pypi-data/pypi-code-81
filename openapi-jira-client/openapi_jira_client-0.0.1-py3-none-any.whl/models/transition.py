from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_transition_type import ComponentsschemasTransitionType
from ..models.screen_id import ScreenID
from ..models.workflow_rules import WorkflowRules
from ..types import UNSET, Unset

T = TypeVar("T", bound="Transition")


@attr.s(auto_attribs=True)
class Transition:
    """ Details of a workflow transition. """

    id_: str
    name: str
    description: str
    from_: List[str]
    to: str
    type_: ComponentsschemasTransitionType
    screen: Union[Unset, ScreenID] = UNSET
    rules: Union[Unset, WorkflowRules] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        description = self.description
        from_ = self.from_

        to = self.to
        type_ = self.type_.value

        screen: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.screen, Unset):
            screen = self.screen.to_dict()

        rules: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = self.rules.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "name": name,
                "description": description,
                "from": from_,
                "to": to,
                "type": type_,
            }
        )
        if screen is not UNSET:
            field_dict["screen"] = screen
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        from_ = cast(List[str], d.pop("from"))

        to = d.pop("to")

        type_ = ComponentsschemasTransitionType(d.pop("type"))

        screen: Union[Unset, ScreenID] = UNSET
        _screen = d.pop("screen", UNSET)
        if not isinstance(_screen, Unset):
            screen = ScreenID.from_dict(_screen)

        rules: Union[Unset, WorkflowRules] = UNSET
        _rules = d.pop("rules", UNSET)
        if not isinstance(_rules, Unset):
            rules = WorkflowRules.from_dict(_rules)

        transition = cls(
            id_=id_,
            name=name,
            description=description,
            from_=from_,
            to=to,
            type_=type_,
            screen=screen,
            rules=rules,
        )

        return transition
