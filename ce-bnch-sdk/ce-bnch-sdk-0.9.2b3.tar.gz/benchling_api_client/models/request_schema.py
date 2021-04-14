from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.request_schema_organization import RequestSchemaOrganization
from ..models.request_schema_type import RequestSchemaType
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestSchema")


@attr.s(auto_attribs=True)
class RequestSchema:
    """  """

    field_definitions: List[SchemaField]
    id: str
    name: str
    type: RequestSchemaType
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    derived_from: Union[Unset, None, str] = UNSET
    organization: Union[Unset, RequestSchemaOrganization] = UNSET
    sql_id: Union[Unset, None, str] = UNSET
    system_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        field_definitions = []
        for field_definitions_item_data in self.field_definitions:
            field_definitions_item = field_definitions_item_data.to_dict()

            field_definitions.append(field_definitions_item)

        id = self.id
        name = self.name
        type = self.type.value

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        derived_from = self.derived_from
        organization: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.organization, Unset):
            organization = self.organization.to_dict()

        sql_id = self.sql_id
        system_name = self.system_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fieldDefinitions": field_definitions,
                "id": id,
                "name": name,
                "type": type,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if derived_from is not UNSET:
            field_dict["derivedFrom"] = derived_from
        if organization is not UNSET:
            field_dict["organization"] = organization
        if sql_id is not UNSET:
            field_dict["sqlId"] = sql_id
        if system_name is not UNSET:
            field_dict["systemName"] = system_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions")
        for field_definitions_item_data in _field_definitions:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        id = d.pop("id")

        name = d.pop("name")

        type = RequestSchemaType(d.pop("type"))

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        derived_from = d.pop("derivedFrom", UNSET)

        organization: Union[Unset, RequestSchemaOrganization] = UNSET
        _organization = d.pop("organization", UNSET)
        if not isinstance(_organization, Unset):
            organization = RequestSchemaOrganization.from_dict(_organization)

        sql_id = d.pop("sqlId", UNSET)

        system_name = d.pop("systemName", UNSET)

        request_schema = cls(
            field_definitions=field_definitions,
            id=id,
            name=name,
            type=type,
            archive_record=archive_record,
            derived_from=derived_from,
            organization=organization,
            sql_id=sql_id,
            system_name=system_name,
        )

        return request_schema
