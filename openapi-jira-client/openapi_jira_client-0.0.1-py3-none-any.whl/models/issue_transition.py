from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.componentsschemas_issue_transition_fields import ComponentsschemasIssueTransitionFields
from ..models.status_details import StatusDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTransition")


@attr.s(auto_attribs=True)
class IssueTransition:
    """ Details of an issue transition. """

    id_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    to: Union[Unset, StatusDetails] = UNSET
    has_screen: Union[Unset, bool] = UNSET
    is_global: Union[Unset, bool] = UNSET
    is_initial: Union[Unset, bool] = UNSET
    is_available: Union[Unset, bool] = UNSET
    is_conditional: Union[Unset, bool] = UNSET
    fields: Union[Unset, ComponentsschemasIssueTransitionFields] = UNSET
    expand: Union[Unset, str] = UNSET
    looped: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        to: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.to, Unset):
            to = self.to.to_dict()

        has_screen = self.has_screen
        is_global = self.is_global
        is_initial = self.is_initial
        is_available = self.is_available
        is_conditional = self.is_conditional
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        expand = self.expand
        looped = self.looped

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if to is not UNSET:
            field_dict["to"] = to
        if has_screen is not UNSET:
            field_dict["hasScreen"] = has_screen
        if is_global is not UNSET:
            field_dict["isGlobal"] = is_global
        if is_initial is not UNSET:
            field_dict["isInitial"] = is_initial
        if is_available is not UNSET:
            field_dict["isAvailable"] = is_available
        if is_conditional is not UNSET:
            field_dict["isConditional"] = is_conditional
        if fields is not UNSET:
            field_dict["fields"] = fields
        if expand is not UNSET:
            field_dict["expand"] = expand
        if looped is not UNSET:
            field_dict["looped"] = looped

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        to: Union[Unset, StatusDetails] = UNSET
        _to = d.pop("to", UNSET)
        if not isinstance(_to, Unset):
            to = StatusDetails.from_dict(_to)

        has_screen = d.pop("hasScreen", UNSET)

        is_global = d.pop("isGlobal", UNSET)

        is_initial = d.pop("isInitial", UNSET)

        is_available = d.pop("isAvailable", UNSET)

        is_conditional = d.pop("isConditional", UNSET)

        fields: Union[Unset, ComponentsschemasIssueTransitionFields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = ComponentsschemasIssueTransitionFields.from_dict(_fields)

        expand = d.pop("expand", UNSET)

        looped = d.pop("looped", UNSET)

        issue_transition = cls(
            id_=id_,
            name=name,
            to=to,
            has_screen=has_screen,
            is_global=is_global,
            is_initial=is_initial,
            is_available=is_available,
            is_conditional=is_conditional,
            fields=fields,
            expand=expand,
            looped=looped,
        )

        issue_transition.additional_properties = d
        return issue_transition

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
