from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.bulk_project_permissions import BulkProjectPermissions
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkPermissionsRequestBean")


@attr.s(auto_attribs=True)
class BulkPermissionsRequestBean:
    """ Details of global permissions to look up and project permissions with associated projects and issues to look up. """

    project_permissions: Union[Unset, List[BulkProjectPermissions]] = UNSET
    global_permissions: Union[Unset, List[str]] = UNSET
    account_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        project_permissions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.project_permissions, Unset):
            project_permissions = []
            for project_permissions_item_data in self.project_permissions:
                project_permissions_item = project_permissions_item_data.to_dict()

                project_permissions.append(project_permissions_item)

        global_permissions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.global_permissions, Unset):
            global_permissions = self.global_permissions

        account_id = self.account_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if project_permissions is not UNSET:
            field_dict["projectPermissions"] = project_permissions
        if global_permissions is not UNSET:
            field_dict["globalPermissions"] = global_permissions
        if account_id is not UNSET:
            field_dict["accountId"] = account_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_permissions = []
        _project_permissions = d.pop("projectPermissions", UNSET)
        for project_permissions_item_data in _project_permissions or []:
            project_permissions_item = BulkProjectPermissions.from_dict(project_permissions_item_data)

            project_permissions.append(project_permissions_item)

        global_permissions = cast(List[str], d.pop("globalPermissions", UNSET))

        account_id = d.pop("accountId", UNSET)

        bulk_permissions_request_bean = cls(
            project_permissions=project_permissions,
            global_permissions=global_permissions,
            account_id=account_id,
        )

        return bulk_permissions_request_bean
