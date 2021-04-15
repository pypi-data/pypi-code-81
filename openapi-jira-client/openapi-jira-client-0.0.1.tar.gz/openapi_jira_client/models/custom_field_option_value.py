from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldOptionValue")


@attr.s(auto_attribs=True)
class CustomFieldOptionValue:
    """ Value of a custom field option and the values of its cascading options. """

    value: str
    cascading_options: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        cascading_options: Union[Unset, List[str]] = UNSET
        if not isinstance(self.cascading_options, Unset):
            cascading_options = self.cascading_options

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
            }
        )
        if cascading_options is not UNSET:
            field_dict["cascadingOptions"] = cascading_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        cascading_options = cast(List[str], d.pop("cascadingOptions", UNSET))

        custom_field_option_value = cls(
            value=value,
            cascading_options=cascading_options,
        )

        return custom_field_option_value
