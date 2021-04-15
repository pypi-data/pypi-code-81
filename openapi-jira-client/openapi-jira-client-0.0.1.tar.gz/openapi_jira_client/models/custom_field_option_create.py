from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldOptionCreate")


@attr.s(auto_attribs=True)
class CustomFieldOptionCreate:
    """ Details of a custom field option to create. """

    value: str
    option_id: Union[Unset, str] = UNSET
    disabled: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        option_id = self.option_id
        disabled = self.disabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
            }
        )
        if option_id is not UNSET:
            field_dict["optionId"] = option_id
        if disabled is not UNSET:
            field_dict["disabled"] = disabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        option_id = d.pop("optionId", UNSET)

        disabled = d.pop("disabled", UNSET)

        custom_field_option_create = cls(
            value=value,
            option_id=option_id,
            disabled=disabled,
        )

        return custom_field_option_create
