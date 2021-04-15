from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PropertyKey")


@attr.s(auto_attribs=True)
class PropertyKey:
    """ Property key details. """

    self_: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        key = self.key

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if key is not UNSET:
            field_dict["key"] = key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        key = d.pop("key", UNSET)

        property_key = cls(
            self_=self_,
            key=key,
        )

        return property_key
