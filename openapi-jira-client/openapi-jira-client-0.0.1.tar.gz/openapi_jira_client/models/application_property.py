from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplicationProperty")


@attr.s(auto_attribs=True)
class ApplicationProperty:
    """ Details of an application property. """

    id_: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    desc: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    default_value: Union[Unset, str] = UNSET
    example: Union[Unset, str] = UNSET
    allowed_values: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        key = self.key
        value = self.value
        name = self.name
        desc = self.desc
        type_ = self.type_
        default_value = self.default_value
        example = self.example
        allowed_values: Union[Unset, List[str]] = UNSET
        if not isinstance(self.allowed_values, Unset):
            allowed_values = self.allowed_values

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value
        if name is not UNSET:
            field_dict["name"] = name
        if desc is not UNSET:
            field_dict["desc"] = desc
        if type_ is not UNSET:
            field_dict["type"] = type_
        if default_value is not UNSET:
            field_dict["defaultValue"] = default_value
        if example is not UNSET:
            field_dict["example"] = example
        if allowed_values is not UNSET:
            field_dict["allowedValues"] = allowed_values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        value = d.pop("value", UNSET)

        name = d.pop("name", UNSET)

        desc = d.pop("desc", UNSET)

        type_ = d.pop("type", UNSET)

        default_value = d.pop("defaultValue", UNSET)

        example = d.pop("example", UNSET)

        allowed_values = cast(List[str], d.pop("allowedValues", UNSET))

        application_property = cls(
            id_=id_,
            key=key,
            value=value,
            name=name,
            desc=desc,
            type_=type_,
            default_value=default_value,
            example=example,
            allowed_values=allowed_values,
        )

        return application_property
