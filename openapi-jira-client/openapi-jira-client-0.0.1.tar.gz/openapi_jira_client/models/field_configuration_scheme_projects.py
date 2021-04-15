from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.field_configuration_scheme import FieldConfigurationScheme
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldConfigurationSchemeProjects")


@attr.s(auto_attribs=True)
class FieldConfigurationSchemeProjects:
    """ Project list with assigned field configuration schema. """

    project_ids: List[str]
    field_configuration_scheme: Union[Unset, FieldConfigurationScheme] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        project_ids = self.project_ids

        field_configuration_scheme: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.field_configuration_scheme, Unset):
            field_configuration_scheme = self.field_configuration_scheme.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectIds": project_ids,
            }
        )
        if field_configuration_scheme is not UNSET:
            field_dict["fieldConfigurationScheme"] = field_configuration_scheme

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_ids = cast(List[str], d.pop("projectIds"))

        field_configuration_scheme: Union[Unset, FieldConfigurationScheme] = UNSET
        _field_configuration_scheme = d.pop("fieldConfigurationScheme", UNSET)
        if not isinstance(_field_configuration_scheme, Unset):
            field_configuration_scheme = FieldConfigurationScheme.from_dict(_field_configuration_scheme)

        field_configuration_scheme_projects = cls(
            project_ids=project_ids,
            field_configuration_scheme=field_configuration_scheme,
        )

        return field_configuration_scheme_projects
