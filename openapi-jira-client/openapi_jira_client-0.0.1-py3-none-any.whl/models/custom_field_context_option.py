from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldContextOption")


@attr.s(auto_attribs=True)
class CustomFieldContextOption:
    """ Details of the custom field options for a context. """

    id_: str
    value: str
    disabled: bool
    option_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        value = self.value
        disabled = self.disabled
        option_id = self.option_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "value": value,
                "disabled": disabled,
            }
        )
        if option_id is not UNSET:
            field_dict["optionId"] = option_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        value = d.pop("value")

        disabled = d.pop("disabled")

        option_id = d.pop("optionId", UNSET)

        custom_field_context_option = cls(
            id_=id_,
            value=value,
            disabled=disabled,
            option_id=option_id,
        )

        return custom_field_context_option
