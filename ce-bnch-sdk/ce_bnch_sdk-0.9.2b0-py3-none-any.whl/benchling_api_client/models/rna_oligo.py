import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.archive_record import ArchiveRecord
from ..models.custom_fields import CustomFields
from ..models.fields import Fields
from ..models.oligo_nucleotide_type import OligoNucleotideType
from ..models.registration_origin import RegistrationOrigin
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="RnaOligo")


@attr.s(auto_attribs=True)
class RnaOligo:
    """  """

    fields: Fields
    id: str
    registration_origin: Optional[RegistrationOrigin]
    api_url: Union[Unset, str] = UNSET
    bases: Union[Unset, str] = UNSET
    aliases: Union[Unset, List[str]] = UNSET
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    custom_fields: Union[Unset, CustomFields] = UNSET
    entity_registry_id: Union[Unset, None, str] = UNSET
    folder_id: Union[Unset, str] = UNSET
    length: Union[Unset, int] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    nucleotide_type: Union[Unset, OligoNucleotideType] = UNSET
    registry_id: Union[Unset, None, str] = UNSET
    schema: Union[Unset, None, SchemaSummary] = UNSET
    web_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        fields = self.fields.to_dict()

        id = self.id
        registration_origin = self.registration_origin.to_dict() if self.registration_origin else None

        api_url = self.api_url
        bases = self.bases
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = self.custom_fields.to_dict()

        entity_registry_id = self.entity_registry_id
        folder_id = self.folder_id
        length = self.length
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        name = self.name
        nucleotide_type: Union[Unset, int] = UNSET
        if not isinstance(self.nucleotide_type, Unset):
            nucleotide_type = self.nucleotide_type.value

        registry_id = self.registry_id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fields": fields,
                "id": id,
                "registrationOrigin": registration_origin,
            }
        )
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url
        if bases is not UNSET:
            field_dict["bases"] = bases
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if length is not UNSET:
            field_dict["length"] = length
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if nucleotide_type is not UNSET:
            field_dict["nucleotideType"] = nucleotide_type
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id")

        registration_origin = None
        _registration_origin = d.pop("registrationOrigin")
        if _registration_origin is not None:
            registration_origin = RegistrationOrigin.from_dict(_registration_origin)

        api_url = d.pop("apiURL", UNSET)

        bases = d.pop("bases", UNSET)

        aliases = cast(List[str], d.pop("aliases", UNSET))

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

        custom_fields: Union[Unset, CustomFields] = UNSET
        _custom_fields = d.pop("customFields", UNSET)
        if not isinstance(_custom_fields, Unset):
            custom_fields = CustomFields.from_dict(_custom_fields)

        entity_registry_id = d.pop("entityRegistryId", UNSET)

        folder_id = d.pop("folderId", UNSET)

        length = d.pop("length", UNSET)

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        name = d.pop("name", UNSET)

        nucleotide_type = None
        _nucleotide_type = d.pop("nucleotideType", UNSET)
        if _nucleotide_type is not None and _nucleotide_type is not UNSET:
            nucleotide_type = OligoNucleotideType(_nucleotide_type)

        registry_id = d.pop("registryId", UNSET)

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = SchemaSummary.from_dict(_schema)

        web_url = d.pop("webURL", UNSET)

        rna_oligo = cls(
            fields=fields,
            id=id,
            registration_origin=registration_origin,
            api_url=api_url,
            bases=bases,
            aliases=aliases,
            archive_record=archive_record,
            created_at=created_at,
            creator=creator,
            custom_fields=custom_fields,
            entity_registry_id=entity_registry_id,
            folder_id=folder_id,
            length=length,
            modified_at=modified_at,
            name=name,
            nucleotide_type=nucleotide_type,
            registry_id=registry_id,
            schema=schema,
            web_url=web_url,
        )

        rna_oligo.additional_properties = d
        return rna_oligo

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
