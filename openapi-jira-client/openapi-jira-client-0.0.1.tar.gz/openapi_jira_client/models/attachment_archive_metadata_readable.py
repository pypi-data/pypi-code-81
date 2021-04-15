from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.attachment_archive_item_readable import AttachmentArchiveItemReadable
from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentArchiveMetadataReadable")


@attr.s(auto_attribs=True)
class AttachmentArchiveMetadataReadable:
    """ Metadata for an archive (for example a zip) and its contents. """

    id_: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    entries: Union[Unset, List[AttachmentArchiveItemReadable]] = UNSET
    total_entry_count: Union[Unset, int] = UNSET
    media_type: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        entries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.entries, Unset):
            entries = []
            for entries_item_data in self.entries:
                entries_item = entries_item_data.to_dict()

                entries.append(entries_item)

        total_entry_count = self.total_entry_count
        media_type = self.media_type

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if entries is not UNSET:
            field_dict["entries"] = entries
        if total_entry_count is not UNSET:
            field_dict["totalEntryCount"] = total_entry_count
        if media_type is not UNSET:
            field_dict["mediaType"] = media_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        entries = []
        _entries = d.pop("entries", UNSET)
        for entries_item_data in _entries or []:
            entries_item = AttachmentArchiveItemReadable.from_dict(entries_item_data)

            entries.append(entries_item)

        total_entry_count = d.pop("totalEntryCount", UNSET)

        media_type = d.pop("mediaType", UNSET)

        attachment_archive_metadata_readable = cls(
            id_=id_,
            name=name,
            entries=entries,
            total_entry_count=total_entry_count,
            media_type=media_type,
        )

        return attachment_archive_metadata_readable
