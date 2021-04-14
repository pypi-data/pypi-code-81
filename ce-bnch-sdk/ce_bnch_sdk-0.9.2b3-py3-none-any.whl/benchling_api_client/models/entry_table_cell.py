from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.entry_link import EntryLink
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryTableCell")


@attr.s(auto_attribs=True)
class EntryTableCell:
    """  """

    link: Union[Unset, EntryLink] = UNSET
    text: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        link: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.link, Unset):
            link = self.link.to_dict()

        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if link is not UNSET:
            field_dict["link"] = link
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        link: Union[Unset, EntryLink] = UNSET
        _link = d.pop("link", UNSET)
        if not isinstance(_link, Unset):
            link = EntryLink.from_dict(_link)

        text = d.pop("text", UNSET)

        entry_table_cell = cls(
            link=link,
            text=text,
        )

        return entry_table_cell
