from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.renamed_option import RenamedOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateCustomFieldOption")


@attr.s(auto_attribs=True)
class UpdateCustomFieldOption:
    """ Details of the options to update for a custom field. """

    options: Union[Unset, List[RenamedOption]] = UNSET

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
            options_item = RenamedOption.from_dict(options_item_data)

            options.append(options_item)

        update_custom_field_option = cls(
            options=options,
        )

        return update_custom_field_option
