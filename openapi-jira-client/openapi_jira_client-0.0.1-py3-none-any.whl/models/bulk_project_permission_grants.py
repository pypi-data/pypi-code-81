from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="BulkProjectPermissionGrants")


@attr.s(auto_attribs=True)
class BulkProjectPermissionGrants:
    """ List of project permissions and the projects and issues those permissions grant access to. """

    permission: str
    issues: List[int]
    projects: List[int]

    def to_dict(self) -> Dict[str, Any]:
        permission = self.permission
        issues = self.issues

        projects = self.projects

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "permission": permission,
                "issues": issues,
                "projects": projects,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permission = d.pop("permission")

        issues = cast(List[int], d.pop("issues"))

        projects = cast(List[int], d.pop("projects"))

        bulk_project_permission_grants = cls(
            permission=permission,
            issues=issues,
            projects=projects,
        )

        return bulk_project_permission_grants
