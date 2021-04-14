from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.assay_run_schema_automation_input_file_configs_item import (
    AssayRunSchemaAutomationInputFileConfigsItem,
)
from ..models.assay_run_schema_automation_output_file_configs_item import (
    AssayRunSchemaAutomationOutputFileConfigsItem,
)
from ..models.assay_run_schema_organization import AssayRunSchemaOrganization
from ..models.assay_run_schema_type import AssayRunSchemaType
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunSchema")


@attr.s(auto_attribs=True)
class AssayRunSchema:
    """  """

    field_definitions: List[SchemaField]
    id: str
    name: str
    type: AssayRunSchemaType
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    automation_input_file_configs: Union[Unset, List[AssayRunSchemaAutomationInputFileConfigsItem]] = UNSET
    automation_output_file_configs: Union[Unset, List[AssayRunSchemaAutomationOutputFileConfigsItem]] = UNSET
    derived_from: Union[Unset, None, str] = UNSET
    organization: Union[Unset, AssayRunSchemaOrganization] = UNSET
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

        automation_input_file_configs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.automation_input_file_configs, Unset):
            automation_input_file_configs = []
            for automation_input_file_configs_item_data in self.automation_input_file_configs:
                automation_input_file_configs_item = automation_input_file_configs_item_data.to_dict()

                automation_input_file_configs.append(automation_input_file_configs_item)

        automation_output_file_configs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.automation_output_file_configs, Unset):
            automation_output_file_configs = []
            for automation_output_file_configs_item_data in self.automation_output_file_configs:
                automation_output_file_configs_item = automation_output_file_configs_item_data.to_dict()

                automation_output_file_configs.append(automation_output_file_configs_item)

        derived_from = self.derived_from
        organization: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.organization, Unset):
            organization = self.organization.to_dict()

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
        if automation_input_file_configs is not UNSET:
            field_dict["automationInputFileConfigs"] = automation_input_file_configs
        if automation_output_file_configs is not UNSET:
            field_dict["automationOutputFileConfigs"] = automation_output_file_configs
        if derived_from is not UNSET:
            field_dict["derivedFrom"] = derived_from
        if organization is not UNSET:
            field_dict["organization"] = organization
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

        type = AssayRunSchemaType(d.pop("type"))

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        automation_input_file_configs = []
        _automation_input_file_configs = d.pop("automationInputFileConfigs", UNSET)
        for automation_input_file_configs_item_data in _automation_input_file_configs or []:
            automation_input_file_configs_item = AssayRunSchemaAutomationInputFileConfigsItem.from_dict(
                automation_input_file_configs_item_data
            )

            automation_input_file_configs.append(automation_input_file_configs_item)

        automation_output_file_configs = []
        _automation_output_file_configs = d.pop("automationOutputFileConfigs", UNSET)
        for automation_output_file_configs_item_data in _automation_output_file_configs or []:
            automation_output_file_configs_item = AssayRunSchemaAutomationOutputFileConfigsItem.from_dict(
                automation_output_file_configs_item_data
            )

            automation_output_file_configs.append(automation_output_file_configs_item)

        derived_from = d.pop("derivedFrom", UNSET)

        organization: Union[Unset, AssayRunSchemaOrganization] = UNSET
        _organization = d.pop("organization", UNSET)
        if not isinstance(_organization, Unset):
            organization = AssayRunSchemaOrganization.from_dict(_organization)

        system_name = d.pop("systemName", UNSET)

        assay_run_schema = cls(
            field_definitions=field_definitions,
            id=id,
            name=name,
            type=type,
            archive_record=archive_record,
            automation_input_file_configs=automation_input_file_configs,
            automation_output_file_configs=automation_output_file_configs,
            derived_from=derived_from,
            organization=organization,
            system_name=system_name,
        )

        return assay_run_schema
