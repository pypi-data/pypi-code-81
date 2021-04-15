from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.bulk_project_permission_grants import BulkProjectPermissionGrants

T = TypeVar("T", bound="BulkPermissionGrants")


@attr.s(auto_attribs=True)
class BulkPermissionGrants:
    """ Details of global and project permissions granted to the user. """

    project_permissions: List[BulkProjectPermissionGrants]
    global_permissions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        project_permissions = []
        for project_permissions_item_data in self.project_permissions:
            project_permissions_item = project_permissions_item_data.to_dict()

            project_permissions.append(project_permissions_item)

        global_permissions = self.global_permissions

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectPermissions": project_permissions,
                "globalPermissions": global_permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_permissions = []
        _project_permissions = d.pop("projectPermissions")
        for project_permissions_item_data in _project_permissions:
            project_permissions_item = BulkProjectPermissionGrants.from_dict(project_permissions_item_data)

            project_permissions.append(project_permissions_item)

        global_permissions = cast(List[str], d.pop("globalPermissions"))

        bulk_permission_grants = cls(
            project_permissions=project_permissions,
            global_permissions=global_permissions,
        )

        return bulk_permission_grants
