from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.renamed_cascading_option import RenamedCascadingOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="RenamedOption")


@attr.s(auto_attribs=True)
class RenamedOption:
    """ Details of a custom field option to rename. """

    value: str
    new_value: str
    cascading_options: Union[Unset, List[RenamedCascadingOption]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        new_value = self.new_value
        cascading_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.cascading_options, Unset):
            cascading_options = []
            for cascading_options_item_data in self.cascading_options:
                cascading_options_item = cascading_options_item_data.to_dict()

                cascading_options.append(cascading_options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
                "newValue": new_value,
            }
        )
        if cascading_options is not UNSET:
            field_dict["cascadingOptions"] = cascading_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        new_value = d.pop("newValue")

        cascading_options = []
        _cascading_options = d.pop("cascadingOptions", UNSET)
        for cascading_options_item_data in _cascading_options or []:
            cascading_options_item = RenamedCascadingOption.from_dict(cascading_options_item_data)

            cascading_options.append(cascading_options_item)

        renamed_option = cls(
            value=value,
            new_value=new_value,
            cascading_options=cascading_options,
        )

        return renamed_option
