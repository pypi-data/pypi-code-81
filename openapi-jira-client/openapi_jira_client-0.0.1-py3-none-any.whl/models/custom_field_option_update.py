from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldOptionUpdate")


@attr.s(auto_attribs=True)
class CustomFieldOptionUpdate:
    """ Details of a custom field option for a context. """

    id_: str
    value: Union[Unset, str] = UNSET
    disabled: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        value = self.value
        disabled = self.disabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value
        if disabled is not UNSET:
            field_dict["disabled"] = disabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        value = d.pop("value", UNSET)

        disabled = d.pop("disabled", UNSET)

        custom_field_option_update = cls(
            id_=id_,
            value=value,
            disabled=disabled,
        )

        return custom_field_option_update
