from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.assay_fields_create import AssayFieldsCreate
from ..models.assay_run_create_validation_status import AssayRunCreateValidationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunCreate")


@attr.s(auto_attribs=True)
class AssayRunCreate:
    """  """

    fields: AssayFieldsCreate
    schema_id: str
    id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    validation_comment: Union[Unset, str] = UNSET
    validation_status: Union[Unset, AssayRunCreateValidationStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields = self.fields.to_dict()

        schema_id = self.schema_id
        id = self.id
        project_id = self.project_id
        validation_comment = self.validation_comment
        validation_status: Union[Unset, int] = UNSET
        if not isinstance(self.validation_status, Unset):
            validation_status = self.validation_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
                "schemaId": schema_id,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment
        if validation_status is not UNSET:
            field_dict["validationStatus"] = validation_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = AssayFieldsCreate.from_dict(d.pop("fields"))

        schema_id = d.pop("schemaId")

        id = d.pop("id", UNSET)

        project_id = d.pop("projectId", UNSET)

        validation_comment = d.pop("validationComment", UNSET)

        validation_status = None
        _validation_status = d.pop("validationStatus", UNSET)
        if _validation_status is not None and _validation_status is not UNSET:
            validation_status = AssayRunCreateValidationStatus(_validation_status)

        assay_run_create = cls(
            fields=fields,
            schema_id=schema_id,
            id=id,
            project_id=project_id,
            validation_comment=validation_comment,
            validation_status=validation_status,
        )

        return assay_run_create
