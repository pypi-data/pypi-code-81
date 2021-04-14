from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.dropdown_option import DropdownOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="Dropdown")


@attr.s(auto_attribs=True)
class Dropdown:
    """  """

    id: str
    name: str
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    options: Union[Unset, List[DropdownOption]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        options: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()

                options.append(options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = DropdownOption.from_dict(options_item_data)

            options.append(options_item)

        dropdown = cls(
            id=id,
            name=name,
            archive_record=archive_record,
            options=options,
        )

        return dropdown
