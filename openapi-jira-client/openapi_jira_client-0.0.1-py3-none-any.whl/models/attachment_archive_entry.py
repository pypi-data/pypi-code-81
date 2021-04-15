from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentArchiveEntry")


@attr.s(auto_attribs=True)
class AttachmentArchiveEntry:
    """  """

    abbreviated_name: Union[Unset, str] = UNSET
    entry_index: Union[Unset, int] = UNSET
    media_type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        abbreviated_name = self.abbreviated_name
        entry_index = self.entry_index
        media_type = self.media_type
        name = self.name
        size = self.size

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if abbreviated_name is not UNSET:
            field_dict["abbreviatedName"] = abbreviated_name
        if entry_index is not UNSET:
            field_dict["entryIndex"] = entry_index
        if media_type is not UNSET:
            field_dict["mediaType"] = media_type
        if name is not UNSET:
            field_dict["name"] = name
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        abbreviated_name = d.pop("abbreviatedName", UNSET)

        entry_index = d.pop("entryIndex", UNSET)

        media_type = d.pop("mediaType", UNSET)

        name = d.pop("name", UNSET)

        size = d.pop("size", UNSET)

        attachment_archive_entry = cls(
            abbreviated_name=abbreviated_name,
            entry_index=entry_index,
            media_type=media_type,
            name=name,
            size=size,
        )

        return attachment_archive_entry
