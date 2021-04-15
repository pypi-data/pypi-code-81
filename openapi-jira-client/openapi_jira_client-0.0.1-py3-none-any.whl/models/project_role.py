from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.role_actor import RoleActor
from ..models.scope import Scope
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectRole")


@attr.s(auto_attribs=True)
class ProjectRole:
    """ Details about the roles in a project. """

    self_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    id_: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    actors: Union[Unset, List[RoleActor]] = UNSET
    scope: Union[Unset, Scope] = UNSET
    translated_name: Union[Unset, str] = UNSET
    current_user_role: Union[Unset, bool] = UNSET
    admin: Union[Unset, bool] = UNSET
    role_configurable: Union[Unset, bool] = UNSET
    default: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        name = self.name
        id_ = self.id_
        description = self.description
        actors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.actors, Unset):
            actors = []
            for actors_item_data in self.actors:
                actors_item = actors_item_data.to_dict()

                actors.append(actors_item)

        scope: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.to_dict()

        translated_name = self.translated_name
        current_user_role = self.current_user_role
        admin = self.admin
        role_configurable = self.role_configurable
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
        if actors is not UNSET:
            field_dict["actors"] = actors
        if scope is not UNSET:
            field_dict["scope"] = scope
        if translated_name is not UNSET:
            field_dict["translatedName"] = translated_name
        if current_user_role is not UNSET:
            field_dict["currentUserRole"] = current_user_role
        if admin is not UNSET:
            field_dict["admin"] = admin
        if role_configurable is not UNSET:
            field_dict["roleConfigurable"] = role_configurable
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

        actors = []
        _actors = d.pop("actors", UNSET)
        for actors_item_data in _actors or []:
            actors_item = RoleActor.from_dict(actors_item_data)

            actors.append(actors_item)

        scope: Union[Unset, Scope] = UNSET
        _scope = d.pop("scope", UNSET)
        if not isinstance(_scope, Unset):
            scope = Scope.from_dict(_scope)

        translated_name = d.pop("translatedName", UNSET)

        current_user_role = d.pop("currentUserRole", UNSET)

        admin = d.pop("admin", UNSET)

        role_configurable = d.pop("roleConfigurable", UNSET)

        default = d.pop("default", UNSET)

        project_role = cls(
            self_=self_,
            name=name,
            id_=id_,
            description=description,
            actors=actors,
            scope=scope,
            translated_name=translated_name,
            current_user_role=current_user_role,
            admin=admin,
            role_configurable=role_configurable,
            default=default,
        )

        return project_role
