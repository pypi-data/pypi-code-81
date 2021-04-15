from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_group_label_type import ComponentsschemasGroupLabelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupLabel")


@attr.s(auto_attribs=True)
class GroupLabel:
    """ A group label. """

    text: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    type_: Union[Unset, ComponentsschemasGroupLabelType] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        text = self.text
        title = self.title
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if text is not UNSET:
            field_dict["text"] = text
        if title is not UNSET:
            field_dict["title"] = title
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        text = d.pop("text", UNSET)

        title = d.pop("title", UNSET)

        type_: Union[Unset, ComponentsschemasGroupLabelType] = UNSET
        _type_ = d.pop("type", UNSET)
        if not isinstance(_type_, Unset):
            type_ = ComponentsschemasGroupLabelType(_type_)

        group_label = cls(
            text=text,
            title=title,
            type_=type_,
        )

        return group_label
