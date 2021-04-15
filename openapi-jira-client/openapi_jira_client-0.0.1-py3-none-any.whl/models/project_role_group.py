from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectRoleGroup")


@attr.s(auto_attribs=True)
class ProjectRoleGroup:
    """ Details of the group associated with the role. """

    display_name: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        display_name = self.display_name
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        display_name = d.pop("displayName", UNSET)

        name = d.pop("name", UNSET)

        project_role_group = cls(
            display_name=display_name,
            name=name,
        )

        return project_role_group
