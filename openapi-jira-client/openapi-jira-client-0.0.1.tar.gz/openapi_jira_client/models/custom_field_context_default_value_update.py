from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.custom_field_context_default_value import CustomFieldContextDefaultValue
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldContextDefaultValueUpdate")


@attr.s(auto_attribs=True)
class CustomFieldContextDefaultValueUpdate:
    """ Default values to update. """

    default_values: Union[Unset, List[CustomFieldContextDefaultValue]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        default_values: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.default_values, Unset):
            default_values = []
            for default_values_item_data in self.default_values:
                default_values_item = default_values_item_data.to_dict()

                default_values.append(default_values_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if default_values is not UNSET:
            field_dict["defaultValues"] = default_values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        default_values = []
        _default_values = d.pop("defaultValues", UNSET)
        for default_values_item_data in _default_values or []:
            default_values_item = CustomFieldContextDefaultValue.from_dict(default_values_item_data)

            default_values.append(default_values_item)

        custom_field_context_default_value_update = cls(
            default_values=default_values,
        )

        return custom_field_context_default_value_update
