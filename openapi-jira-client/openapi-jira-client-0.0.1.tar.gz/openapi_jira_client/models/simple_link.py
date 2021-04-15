from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleLink")


@attr.s(auto_attribs=True)
class SimpleLink:
    """ Details about the operations available in this version. """

    id_: Union[Unset, str] = UNSET
    style_class: Union[Unset, str] = UNSET
    icon_class: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    href: Union[Unset, str] = UNSET
    weight: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        style_class = self.style_class
        icon_class = self.icon_class
        label = self.label
        title = self.title
        href = self.href
        weight = self.weight

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if style_class is not UNSET:
            field_dict["styleClass"] = style_class
        if icon_class is not UNSET:
            field_dict["iconClass"] = icon_class
        if label is not UNSET:
            field_dict["label"] = label
        if title is not UNSET:
            field_dict["title"] = title
        if href is not UNSET:
            field_dict["href"] = href
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        style_class = d.pop("styleClass", UNSET)

        icon_class = d.pop("iconClass", UNSET)

        label = d.pop("label", UNSET)

        title = d.pop("title", UNSET)

        href = d.pop("href", UNSET)

        weight = d.pop("weight", UNSET)

        simple_link = cls(
            id_=id_,
            style_class=style_class,
            icon_class=icon_class,
            label=label,
            title=title,
            href=href,
            weight=weight,
        )

        return simple_link
