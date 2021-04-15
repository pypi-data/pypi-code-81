from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectPermissions")


@attr.s(auto_attribs=True)
class ProjectPermissions:
    """ Permissions which a user has on a project. """

    can_edit: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        can_edit = self.can_edit

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if can_edit is not UNSET:
            field_dict["canEdit"] = can_edit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        can_edit = d.pop("canEdit", UNSET)

        project_permissions = cls(
            can_edit=can_edit,
        )

        return project_permissions
