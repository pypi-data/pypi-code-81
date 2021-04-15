from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ColumnItem")


@attr.s(auto_attribs=True)
class ColumnItem:
    """ Details of an issue navigator column item. """

    label: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label", UNSET)

        value = d.pop("value", UNSET)

        column_item = cls(
            label=label,
            value=value,
        )

        return column_item
