from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="RenamedCascadingOption")


@attr.s(auto_attribs=True)
class RenamedCascadingOption:
    """ Details of a custom field cascading option to rename. """

    value: str
    new_value: str

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        new_value = self.new_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
                "newValue": new_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        new_value = d.pop("newValue")

        renamed_cascading_option = cls(
            value=value,
            new_value=new_value,
        )

        return renamed_cascading_option
