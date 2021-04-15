from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.permission_holder import PermissionHolder
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionGrant")


@attr.s(auto_attribs=True)
class PermissionGrant:
    """ Details about a permission granted to a user or group. """

    id_: Union[Unset, int] = UNSET
    self_: Union[Unset, str] = UNSET
    holder: Union[Unset, PermissionHolder] = UNSET
    permission: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        self_ = self.self_
        holder: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.holder, Unset):
            holder = self.holder.to_dict()

        permission = self.permission

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if self_ is not UNSET:
            field_dict["self"] = self_
        if holder is not UNSET:
            field_dict["holder"] = holder
        if permission is not UNSET:
            field_dict["permission"] = permission

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        holder: Union[Unset, PermissionHolder] = UNSET
        _holder = d.pop("holder", UNSET)
        if not isinstance(_holder, Unset):
            holder = PermissionHolder.from_dict(_holder)

        permission = d.pop("permission", UNSET)

        permission_grant = cls(
            id_=id_,
            self_=self_,
            holder=holder,
            permission=permission,
        )

        return permission_grant
