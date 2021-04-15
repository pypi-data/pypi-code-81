from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTransitionProperty")


@attr.s(auto_attribs=True)
class WorkflowTransitionProperty:
    """ Details about the server Jira is running on. """

    value: str
    key: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        key = self.key
        id_ = self.id_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if key is not UNSET:
            field_dict["key"] = key
        if id_ is not UNSET:
            field_dict["id"] = id_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        key = d.pop("key", UNSET)

        id_ = d.pop("id", UNSET)

        workflow_transition_property = cls(
            value=value,
            key=key,
            id_=id_,
        )

        workflow_transition_property.additional_properties = d
        return workflow_transition_property

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
