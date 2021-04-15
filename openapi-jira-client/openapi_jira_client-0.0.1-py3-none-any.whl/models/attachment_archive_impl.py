from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.attachment_archive_entry import AttachmentArchiveEntry
from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentArchiveImpl")


@attr.s(auto_attribs=True)
class AttachmentArchiveImpl:
    """  """

    entries: Union[Unset, List[AttachmentArchiveEntry]] = UNSET
    total_entry_count: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.entries, Unset):
            entries = []
            for entries_item_data in self.entries:
                entries_item = entries_item_data.to_dict()

                entries.append(entries_item)

        total_entry_count = self.total_entry_count

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entries is not UNSET:
            field_dict["entries"] = entries
        if total_entry_count is not UNSET:
            field_dict["totalEntryCount"] = total_entry_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entries = []
        _entries = d.pop("entries", UNSET)
        for entries_item_data in _entries or []:
            entries_item = AttachmentArchiveEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        total_entry_count = d.pop("totalEntryCount", UNSET)

        attachment_archive_impl = cls(
            entries=entries,
            total_entry_count=total_entry_count,
        )

        return attachment_archive_impl
