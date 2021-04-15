from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_share_permission_input_bean_type import ComponentsschemasSharePermissionInputBeanType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SharePermissionInputBean")


@attr.s(auto_attribs=True)
class SharePermissionInputBean:
    """  """

    type_: ComponentsschemasSharePermissionInputBeanType
    project_id: Union[Unset, str] = UNSET
    groupname: Union[Unset, str] = UNSET
    project_role_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type_ = self.type_.value

        project_id = self.project_id
        groupname = self.groupname
        project_role_id = self.project_role_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type_,
            }
        )
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if groupname is not UNSET:
            field_dict["groupname"] = groupname
        if project_role_id is not UNSET:
            field_dict["projectRoleId"] = project_role_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = ComponentsschemasSharePermissionInputBeanType(d.pop("type"))

        project_id = d.pop("projectId", UNSET)

        groupname = d.pop("groupname", UNSET)

        project_role_id = d.pop("projectRoleId", UNSET)

        share_permission_input_bean = cls(
            type_=type_,
            project_id=project_id,
            groupname=groupname,
            project_role_id=project_role_id,
        )

        return share_permission_input_bean
