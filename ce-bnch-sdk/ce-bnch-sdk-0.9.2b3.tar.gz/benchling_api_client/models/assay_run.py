from typing import Any, Dict, Optional, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRun")


@attr.s(auto_attribs=True)
class AssayRun:
    """  """

    fields: Fields
    id: str
    schema: Optional[SchemaSummary]
    api_url: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    created_at: Union[Unset, str] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    entry_id: Union[Unset, str] = UNSET
    is_reviewed: Union[Unset, bool] = UNSET
    project_id: Union[Unset, str] = UNSET
    validation_comment: Union[Unset, str] = UNSET
    validation_schema: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields = self.fields.to_dict()

        id = self.id
        api_url = self.api_url
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        created_at = self.created_at
        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        entry_id = self.entry_id
        is_reviewed = self.is_reviewed
        project_id = self.project_id
        schema = self.schema.to_dict() if self.schema else None

        validation_comment = self.validation_comment
        validation_schema = self.validation_schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
                "id": id,
                "schema": schema,
            }
        )
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if entry_id is not UNSET:
            field_dict["entryId"] = entry_id
        if is_reviewed is not UNSET:
            field_dict["isReviewed"] = is_reviewed
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment
        if validation_schema is not UNSET:
            field_dict["validationSchema"] = validation_schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id")

        api_url = d.pop("apiURL", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        created_at = d.pop("createdAt", UNSET)

        creator: Union[Unset, UserSummary] = UNSET
        _creator = d.pop("creator", UNSET)
        if not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(_creator)

        entry_id = d.pop("entryId", UNSET)

        is_reviewed = d.pop("isReviewed", UNSET)

        project_id = d.pop("projectId", UNSET)

        schema = None
        _schema = d.pop("schema")
        if _schema is not None:
            schema = SchemaSummary.from_dict(_schema)

        validation_comment = d.pop("validationComment", UNSET)

        validation_schema = d.pop("validationSchema", UNSET)

        assay_run = cls(
            fields=fields,
            id=id,
            api_url=api_url,
            archive_record=archive_record,
            created_at=created_at,
            creator=creator,
            entry_id=entry_id,
            is_reviewed=is_reviewed,
            project_id=project_id,
            schema=schema,
            validation_comment=validation_comment,
            validation_schema=validation_schema,
        )

        return assay_run
