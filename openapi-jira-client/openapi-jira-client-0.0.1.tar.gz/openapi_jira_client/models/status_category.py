from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="StatusCategory")


@attr.s(auto_attribs=True)
class StatusCategory:
    """ A status category. """

    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, int] = UNSET
    key: Union[Unset, str] = UNSET
    color_name: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id_ = self.id_
        key = self.key
        color_name = self.color_name
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if key is not UNSET:
            field_dict["key"] = key
        if color_name is not UNSET:
            field_dict["colorName"] = color_name
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        color_name = d.pop("colorName", UNSET)

        name = d.pop("name", UNSET)

        status_category = cls(
            self_=self_,
            id_=id_,
            key=key,
            color_name=color_name,
            name=name,
        )

        status_category.additional_properties = d
        return status_category

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
