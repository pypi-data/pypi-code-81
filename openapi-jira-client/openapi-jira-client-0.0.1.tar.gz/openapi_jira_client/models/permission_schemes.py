from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.permission_scheme import PermissionScheme
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionSchemes")


@attr.s(auto_attribs=True)
class PermissionSchemes:
    """ List of all permission schemes. """

    permission_schemes: Union[Unset, List[PermissionScheme]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        permission_schemes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.permission_schemes, Unset):
            permission_schemes = []
            for permission_schemes_item_data in self.permission_schemes:
                permission_schemes_item = permission_schemes_item_data.to_dict()

                permission_schemes.append(permission_schemes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if permission_schemes is not UNSET:
            field_dict["permissionSchemes"] = permission_schemes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permission_schemes = []
        _permission_schemes = d.pop("permissionSchemes", UNSET)
        for permission_schemes_item_data in _permission_schemes or []:
            permission_schemes_item = PermissionScheme.from_dict(permission_schemes_item_data)

            permission_schemes.append(permission_schemes_item)

        permission_schemes = cls(
            permission_schemes=permission_schemes,
        )

        return permission_schemes
