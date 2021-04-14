import datetime
from typing import Any, cast, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.aa_sequence import AaSequence
from ..models.archive_record import ArchiveRecord
from ..models.custom_entity import CustomEntity
from ..models.dna_sequence import DnaSequence
from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Batch")


@attr.s(auto_attribs=True)
class Batch:
    """  """

    id: str
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    entity: Union[Unset, DnaSequence, AaSequence, CustomEntity] = UNSET
    fields: Union[Unset, Fields] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    schema: Union[Unset, None, SchemaSummary] = UNSET
    web_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        entity: Union[Unset, Dict[str, Any]]
        if isinstance(self.entity, Unset):
            entity = UNSET
        elif isinstance(self.entity, DnaSequence):
            entity = UNSET
            if not isinstance(self.entity, Unset):
                entity = self.entity.to_dict()

        elif isinstance(self.entity, AaSequence):
            entity = UNSET
            if not isinstance(self.entity, Unset):
                entity = self.entity.to_dict()

        else:
            entity = UNSET
            if not isinstance(self.entity, Unset):
                entity = self.entity.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        name = self.name
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if entity is not UNSET:
            field_dict["entity"] = entity
        if fields is not UNSET:
            field_dict["fields"] = fields
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        creator: Union[Unset, UserSummary] = UNSET
        _creator = d.pop("creator", UNSET)
        if not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(_creator)

        def _parse_entity(
            data: Union[Unset, Dict[str, Any]]
        ) -> Union[Unset, DnaSequence, AaSequence, CustomEntity]:
            entity: Union[Unset, DnaSequence, AaSequence, CustomEntity]
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                entity = UNSET
                _entity = data
                if not isinstance(_entity, Unset):
                    entity = DnaSequence.from_dict(_entity)

                return entity
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                entity = UNSET
                _entity = data
                if not isinstance(_entity, Unset):
                    entity = AaSequence.from_dict(_entity)

                return entity
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            entity = UNSET
            _entity = data
            if not isinstance(_entity, Unset):
                entity = CustomEntity.from_dict(_entity)

            return entity

        entity = _parse_entity(d.pop("entity", UNSET))

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        name = d.pop("name", UNSET)

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = SchemaSummary.from_dict(_schema)

        web_url = d.pop("webURL", UNSET)

        batch = cls(
            id=id,
            archive_record=archive_record,
            created_at=created_at,
            creator=creator,
            entity=entity,
            fields=fields,
            modified_at=modified_at,
            name=name,
            schema=schema,
            web_url=web_url,
        )

        return batch
