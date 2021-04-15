from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_permissions_permissions import ComponentsschemasPermissionsPermissions
from ..types import UNSET, Unset

T = TypeVar("T", bound="Permissions")


@attr.s(auto_attribs=True)
class Permissions:
    """ Details about permissions. """

    permissions: Union[Unset, ComponentsschemasPermissionsPermissions] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        permissions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permissions: Union[Unset, ComponentsschemasPermissionsPermissions] = UNSET
        _permissions = d.pop("permissions", UNSET)
        if not isinstance(_permissions, Unset):
            permissions = ComponentsschemasPermissionsPermissions.from_dict(_permissions)

        permissions = cls(
            permissions=permissions,
        )

        return permissions
