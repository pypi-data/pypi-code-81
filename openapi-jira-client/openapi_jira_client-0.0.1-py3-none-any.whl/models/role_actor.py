from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_role_actor_type import ComponentsschemasRoleActorType
from ..models.project_role_group import ProjectRoleGroup
from ..models.project_role_user import ProjectRoleUser
from ..types import UNSET, Unset

T = TypeVar("T", bound="RoleActor")


@attr.s(auto_attribs=True)
class RoleActor:
    """ Details about a user assigned to a project role. """

    id_: Union[Unset, int] = UNSET
    display_name: Union[Unset, str] = UNSET
    type_: Union[Unset, ComponentsschemasRoleActorType] = UNSET
    name: Union[Unset, str] = UNSET
    avatar_url: Union[Unset, str] = UNSET
    actor_user: Union[Unset, ProjectRoleUser] = UNSET
    actor_group: Union[Unset, ProjectRoleGroup] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        display_name = self.display_name
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        name = self.name
        avatar_url = self.avatar_url
        actor_user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.actor_user, Unset):
            actor_user = self.actor_user.to_dict()

        actor_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.actor_group, Unset):
            actor_group = self.actor_group.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if avatar_url is not UNSET:
            field_dict["avatarUrl"] = avatar_url
        if actor_user is not UNSET:
            field_dict["actorUser"] = actor_user
        if actor_group is not UNSET:
            field_dict["actorGroup"] = actor_group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        display_name = d.pop("displayName", UNSET)

        type_: Union[Unset, ComponentsschemasRoleActorType] = UNSET
        _type_ = d.pop("type", UNSET)
        if not isinstance(_type_, Unset):
            type_ = ComponentsschemasRoleActorType(_type_)

        name = d.pop("name", UNSET)

        avatar_url = d.pop("avatarUrl", UNSET)

        actor_user: Union[Unset, ProjectRoleUser] = UNSET
        _actor_user = d.pop("actorUser", UNSET)
        if not isinstance(_actor_user, Unset):
            actor_user = ProjectRoleUser.from_dict(_actor_user)

        actor_group: Union[Unset, ProjectRoleGroup] = UNSET
        _actor_group = d.pop("actorGroup", UNSET)
        if not isinstance(_actor_group, Unset):
            actor_group = ProjectRoleGroup.from_dict(_actor_group)

        role_actor = cls(
            id_=id_,
            display_name=display_name,
            type_=type_,
            name=name,
            avatar_url=avatar_url,
            actor_user=actor_user,
            actor_group=actor_group,
        )

        return role_actor
