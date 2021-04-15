import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.componentsschemas_field_last_used_type import ComponentsschemasFieldLastUsedType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldLastUsed")


@attr.s(auto_attribs=True)
class FieldLastUsed:
    """ Information about the most recent use of a field. """

    type_: Union[Unset, ComponentsschemasFieldLastUsedType] = UNSET
    value: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        value: Union[Unset, str] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type_: Union[Unset, ComponentsschemasFieldLastUsedType] = UNSET
        _type_ = d.pop("type", UNSET)
        if not isinstance(_type_, Unset):
            type_ = ComponentsschemasFieldLastUsedType(_type_)

        value: Union[Unset, datetime.datetime] = UNSET
        _value = d.pop("value", UNSET)
        if not isinstance(_value, Unset):
            value = isoparse(_value)

        field_last_used = cls(
            type_=type_,
            value=value,
        )

        return field_last_used
