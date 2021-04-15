from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldConfigurationSchemeProjectAssociation")


@attr.s(auto_attribs=True)
class FieldConfigurationSchemeProjectAssociation:
    """ Associated field configuration scheme and project. """

    project_id: str
    field_configuration_scheme_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        field_configuration_scheme_id = self.field_configuration_scheme_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectId": project_id,
            }
        )
        if field_configuration_scheme_id is not UNSET:
            field_dict["fieldConfigurationSchemeId"] = field_configuration_scheme_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("projectId")

        field_configuration_scheme_id = d.pop("fieldConfigurationSchemeId", UNSET)

        field_configuration_scheme_project_association = cls(
            project_id=project_id,
            field_configuration_scheme_id=field_configuration_scheme_id,
        )

        return field_configuration_scheme_project_association
