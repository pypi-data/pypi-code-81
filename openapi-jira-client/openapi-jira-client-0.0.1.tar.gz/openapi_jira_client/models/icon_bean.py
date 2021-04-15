from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IconBean")


@attr.s(auto_attribs=True)
class IconBean:
    """ An icon. """

    url16x16: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    link: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        url16x16 = self.url16x16
        title = self.title
        link = self.link

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if url16x16 is not UNSET:
            field_dict["url16x16"] = url16x16
        if title is not UNSET:
            field_dict["title"] = title
        if link is not UNSET:
            field_dict["link"] = link

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url16x16 = d.pop("url16x16", UNSET)

        title = d.pop("title", UNSET)

        link = d.pop("link", UNSET)

        icon_bean = cls(
            url16x16=url16x16,
            title=title,
            link=link,
        )

        return icon_bean
