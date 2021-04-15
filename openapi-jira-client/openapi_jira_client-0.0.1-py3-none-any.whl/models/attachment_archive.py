from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.attachment_archive_entry import AttachmentArchiveEntry
from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentArchive")


@attr.s(auto_attribs=True)
class AttachmentArchive:
    """  """

    more_available: Union[Unset, bool] = UNSET
    total_number_of_entries_available: Union[Unset, int] = UNSET
    total_entry_count: Union[Unset, int] = UNSET
    entries: Union[Unset, List[AttachmentArchiveEntry]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        more_available = self.more_available
        total_number_of_entries_available = self.total_number_of_entries_available
        total_entry_count = self.total_entry_count
        entries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.entries, Unset):
            entries = []
            for entries_item_data in self.entries:
                entries_item = entries_item_data.to_dict()

                entries.append(entries_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if more_available is not UNSET:
            field_dict["moreAvailable"] = more_available
        if total_number_of_entries_available is not UNSET:
            field_dict["totalNumberOfEntriesAvailable"] = total_number_of_entries_available
        if total_entry_count is not UNSET:
            field_dict["totalEntryCount"] = total_entry_count
        if entries is not UNSET:
            field_dict["entries"] = entries

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        more_available = d.pop("moreAvailable", UNSET)

        total_number_of_entries_available = d.pop("totalNumberOfEntriesAvailable", UNSET)

        total_entry_count = d.pop("totalEntryCount", UNSET)

        entries = []
        _entries = d.pop("entries", UNSET)
        for entries_item_data in _entries or []:
            entries_item = AttachmentArchiveEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        attachment_archive = cls(
            more_available=more_available,
            total_number_of_entries_available=total_number_of_entries_available,
            total_entry_count=total_entry_count,
            entries=entries,
        )

        return attachment_archive
