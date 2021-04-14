from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.assay_fields_create import AssayFieldsCreate
from ..models.assay_result_create_field_validation import AssayResultCreateFieldValidation
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayResultCreate")


@attr.s(auto_attribs=True)
class AssayResultCreate:
    """  """

    fields: AssayFieldsCreate
    schema_id: str
    field_validation: Union[Unset, AssayResultCreateFieldValidation] = UNSET
    id: Union[Unset, str] = UNSET
    project_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields = self.fields.to_dict()

        schema_id = self.schema_id
        field_validation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.field_validation, Unset):
            field_validation = self.field_validation.to_dict()

        id = self.id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
                "schemaId": schema_id,
            }
        )
        if field_validation is not UNSET:
            field_dict["fieldValidation"] = field_validation
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = AssayFieldsCreate.from_dict(d.pop("fields"))

        schema_id = d.pop("schemaId")

        field_validation: Union[Unset, AssayResultCreateFieldValidation] = UNSET
        _field_validation = d.pop("fieldValidation", UNSET)
        if not isinstance(_field_validation, Unset):
            field_validation = AssayResultCreateFieldValidation.from_dict(_field_validation)

        id = d.pop("id", UNSET)

        project_id = d.pop("projectId", UNSET)

        assay_result_create = cls(
            fields=fields,
            schema_id=schema_id,
            field_validation=field_validation,
            id=id,
            project_id=project_id,
        )

        return assay_result_create
