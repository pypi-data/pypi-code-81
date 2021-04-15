from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldReplacement")


@attr.s(auto_attribs=True)
class CustomFieldReplacement:
    """ Details about the replacement for a deleted version. """

    custom_field_id: Union[Unset, int] = UNSET
    move_to: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        custom_field_id = self.custom_field_id
        move_to = self.move_to

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if custom_field_id is not UNSET:
            field_dict["customFieldId"] = custom_field_id
        if move_to is not UNSET:
            field_dict["moveTo"] = move_to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom_field_id = d.pop("customFieldId", UNSET)

        move_to = d.pop("moveTo", UNSET)

        custom_field_replacement = cls(
            custom_field_id=custom_field_id,
            move_to=move_to,
        )

        return custom_field_replacement
