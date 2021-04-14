from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="AutomationOutputProcessorCreate")


@attr.s(auto_attribs=True)
class AutomationOutputProcessorCreate:
    """  """

    assay_run_id: str
    automation_file_config_name: str
    file_id: str

    def to_dict(self) -> Dict[str, Any]:
        assay_run_id = self.assay_run_id
        automation_file_config_name = self.automation_file_config_name
        file_id = self.file_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayRunId": assay_run_id,
                "automationFileConfigName": automation_file_config_name,
                "fileId": file_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_run_id = d.pop("assayRunId")

        automation_file_config_name = d.pop("automationFileConfigName")

        file_id = d.pop("fileId")

        automation_output_processor_create = cls(
            assay_run_id=assay_run_id,
            automation_file_config_name=automation_file_config_name,
            file_id=file_id,
        )

        return automation_output_processor_create
