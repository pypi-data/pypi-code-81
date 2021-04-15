from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.scope import Scope
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectRoleDetails")


@attr.s(auto_attribs=True)
class ProjectRoleDetails:
    """ Details about a project role. """

    self_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    id_: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    admin: Union[Unset, bool] = UNSET
    scope: Union[Unset, Scope] = UNSET
    role_configurable: Union[Unset, bool] = UNSET
    translated_name: Union[Unset, str] = UNSET
    default: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        name = self.name
        id_ = self.id_
        description = self.description
        admin = self.admin
        scope: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.to_dict()

        role_configurable = self.role_configurable
        translated_name = self.translated_name
        default = self.default

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if name is not UNSET:
            field_dict["name"] = name
        if id_ is not UNSET:
            field_dict["id"] = id_
        if description is not UNSET:
            field_dict["description"] = description
        if admin is not UNSET:
            field_dict["admin"] = admin
        if scope is not UNSET:
            field_dict["scope"] = scope
        if role_configurable is not UNSET:
            field_dict["roleConfigurable"] = role_configurable
        if translated_name is not UNSET:
            field_dict["translatedName"] = translated_name
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        name = d.pop("name", UNSET)

        id_ = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        admin = d.pop("admin", UNSET)

        scope: Union[Unset, Scope] = UNSET
        _scope = d.pop("scope", UNSET)
        if not isinstance(_scope, Unset):
            scope = Scope.from_dict(_scope)

        role_configurable = d.pop("roleConfigurable", UNSET)

        translated_name = d.pop("translatedName", UNSET)

        default = d.pop("default", UNSET)

        project_role_details = cls(
            self_=self_,
            name=name,
            id_=id_,
            description=description,
            admin=admin,
            scope=scope,
            role_configurable=role_configurable,
            translated_name=translated_name,
            default=default,
        )

        return project_role_details
