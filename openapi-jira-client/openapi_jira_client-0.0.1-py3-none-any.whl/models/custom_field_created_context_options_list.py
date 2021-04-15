from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.custom_field_context_option import CustomFieldContextOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldCreatedContextOptionsList")


@attr.s(auto_attribs=True)
class CustomFieldCreatedContextOptionsList:
    """ A list of custom field options for a context. """

    options: Union[Unset, List[CustomFieldContextOption]] = UNSET

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
            options_item = CustomFieldContextOption.from_dict(options_item_data)

            options.append(options_item)

        custom_field_created_context_options_list = cls(
            options=options,
        )

        return custom_field_created_context_options_list
