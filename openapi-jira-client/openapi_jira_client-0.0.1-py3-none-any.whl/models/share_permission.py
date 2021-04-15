from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_share_permission_type import ComponentsschemasSharePermissionType
from ..models.group_name import GroupName
from ..models.project import Project
from ..models.project_role import ProjectRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="SharePermission")


@attr.s(auto_attribs=True)
class SharePermission:
    """ Details of a share permission for the filter. """

    type_: ComponentsschemasSharePermissionType
    id_: Union[Unset, int] = UNSET
    project: Union[Unset, Project] = UNSET
    role: Union[Unset, ProjectRole] = UNSET
    group: Union[Unset, GroupName] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type_ = self.type_.value

        id_ = self.id_
        project: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.project, Unset):
            project = self.project.to_dict()

        role: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.to_dict()

        group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.group, Unset):
            group = self.group.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type_,
            }
        )
        if id_ is not UNSET:
            field_dict["id"] = id_
        if project is not UNSET:
            field_dict["project"] = project
        if role is not UNSET:
            field_dict["role"] = role
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = ComponentsschemasSharePermissionType(d.pop("type"))

        id_ = d.pop("id", UNSET)

        project: Union[Unset, Project] = UNSET
        _project = d.pop("project", UNSET)
        if not isinstance(_project, Unset):
            project = Project.from_dict(_project)

        role: Union[Unset, ProjectRole] = UNSET
        _role = d.pop("role", UNSET)
        if not isinstance(_role, Unset):
            role = ProjectRole.from_dict(_role)

        group: Union[Unset, GroupName] = UNSET
        _group = d.pop("group", UNSET)
        if not isinstance(_group, Unset):
            group = GroupName.from_dict(_group)

        share_permission = cls(
            type_=type_,
            id_=id_,
            project=project,
            role=role,
            group=group,
        )

        return share_permission
