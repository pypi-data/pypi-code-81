from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldOption")


@attr.s(auto_attribs=True)
class CustomFieldOption:
    """ Details of a custom option for a field. """

    self_: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        value = d.pop("value", UNSET)

        custom_field_option = cls(
            self_=self_,
            value=value,
        )

        return custom_field_option
