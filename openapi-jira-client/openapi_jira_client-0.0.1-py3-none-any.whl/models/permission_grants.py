from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.permission_grant import PermissionGrant
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionGrants")


@attr.s(auto_attribs=True)
class PermissionGrants:
    """ List of permission grants. """

    permissions: Union[Unset, List[PermissionGrant]] = UNSET
    expand: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        permissions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()

                permissions.append(permissions_item)

        expand = self.expand

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if expand is not UNSET:
            field_dict["expand"] = expand

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = PermissionGrant.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        expand = d.pop("expand", UNSET)

        permission_grants = cls(
            permissions=permissions,
            expand=expand,
        )

        return permission_grants
