from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.custom_field_option_value import CustomFieldOptionValue
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkCreateCustomFieldOptionRequest")


@attr.s(auto_attribs=True)
class BulkCreateCustomFieldOptionRequest:
    """ Details of options to create for a custom field. """

    options: Union[Unset, List[CustomFieldOptionValue]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()

                options.append(options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = CustomFieldOptionValue.from_dict(options_item_data)

            options.append(options_item)

        bulk_create_custom_field_option_request = cls(
            options=options,
        )

        return bulk_create_custom_field_option_request
