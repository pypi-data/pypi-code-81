from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.permission_grant import PermissionGrant
from ..models.scope import Scope
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionScheme")


@attr.s(auto_attribs=True)
class PermissionScheme:
    """ Details of a permission scheme. """

    name: str
    expand: Union[Unset, str] = UNSET
    id_: Union[Unset, int] = UNSET
    self_: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    scope: Union[Unset, Scope] = UNSET
    permissions: Union[Unset, List[PermissionGrant]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        expand = self.expand
        id_ = self.id_
        self_ = self.self_
        description = self.description
        scope: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.to_dict()

        permissions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()

                permissions.append(permissions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if expand is not UNSET:
            field_dict["expand"] = expand
        if id_ is not UNSET:
            field_dict["id"] = id_
        if self_ is not UNSET:
            field_dict["self"] = self_
        if description is not UNSET:
            field_dict["description"] = description
        if scope is not UNSET:
            field_dict["scope"] = scope
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        expand = d.pop("expand", UNSET)

        id_ = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        description = d.pop("description", UNSET)

        scope: Union[Unset, Scope] = UNSET
        _scope = d.pop("scope", UNSET)
        if not isinstance(_scope, Unset):
            scope = Scope.from_dict(_scope)

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = PermissionGrant.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        permission_scheme = cls(
            name=name,
            expand=expand,
            id_=id_,
            self_=self_,
            description=description,
            scope=scope,
            permissions=permissions,
        )

        permission_scheme.additional_properties = d
        return permission_scheme

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
