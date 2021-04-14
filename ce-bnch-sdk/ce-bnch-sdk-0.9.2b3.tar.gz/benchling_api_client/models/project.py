from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.organization import Organization
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Project")


@attr.s(auto_attribs=True)
class Project:
    """  """

    id: str
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    name: Union[Unset, str] = UNSET
    owner: Union[Unset, Organization, UserSummary] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        name = self.name
        owner: Union[Unset, Dict[str, Any]]
        if isinstance(self.owner, Unset):
            owner = UNSET
        elif isinstance(self.owner, Organization):
            owner = UNSET
            if not isinstance(self.owner, Unset):
                owner = self.owner.to_dict()

        else:
            owner = UNSET
            if not isinstance(self.owner, Unset):
                owner = self.owner.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if name is not UNSET:
            field_dict["name"] = name
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        name = d.pop("name", UNSET)

        def _parse_owner(data: Union[Unset, Dict[str, Any]]) -> Union[Unset, Organization, UserSummary]:
            owner: Union[Unset, Organization, UserSummary]
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                owner = UNSET
                _owner = data
                if not isinstance(_owner, Unset):
                    owner = Organization.from_dict(_owner)

                return owner
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            owner = UNSET
            _owner = data
            if not isinstance(_owner, Unset):
                owner = UserSummary.from_dict(_owner)

            return owner

        owner = _parse_owner(d.pop("owner", UNSET))

        project = cls(
            id=id,
            archive_record=archive_record,
            name=name,
            owner=owner,
        )

        return project
