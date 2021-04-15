from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkProjectPermissions")


@attr.s(auto_attribs=True)
class BulkProjectPermissions:
    """ Details of project permissions and associated issues and projects to look up. """

    permissions: List[str]
    issues: Union[Unset, List[int]] = UNSET
    projects: Union[Unset, List[int]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        permissions = self.permissions

        issues: Union[Unset, List[int]] = UNSET
        if not isinstance(self.issues, Unset):
            issues = self.issues

        projects: Union[Unset, List[int]] = UNSET
        if not isinstance(self.projects, Unset):
            projects = self.projects

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "permissions": permissions,
            }
        )
        if issues is not UNSET:
            field_dict["issues"] = issues
        if projects is not UNSET:
            field_dict["projects"] = projects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permissions = cast(List[str], d.pop("permissions"))

        issues = cast(List[int], d.pop("issues", UNSET))

        projects = cast(List[int], d.pop("projects", UNSET))

        bulk_project_permissions = cls(
            permissions=permissions,
            issues=issues,
            projects=projects,
        )

        return bulk_project_permissions
