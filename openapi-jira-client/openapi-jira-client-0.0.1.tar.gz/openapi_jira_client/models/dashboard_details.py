from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.share_permission import SharePermission
from ..types import UNSET, Unset

T = TypeVar("T", bound="DashboardDetails")


@attr.s(auto_attribs=True)
class DashboardDetails:
    """ Details of a dashboard. """

    name: str
    share_permissions: List[SharePermission]
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        share_permissions = []
        for share_permissions_item_data in self.share_permissions:
            share_permissions_item = share_permissions_item_data.to_dict()

            share_permissions.append(share_permissions_item)

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "sharePermissions": share_permissions,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        share_permissions = []
        _share_permissions = d.pop("sharePermissions")
        for share_permissions_item_data in _share_permissions:
            share_permissions_item = SharePermission.from_dict(share_permissions_item_data)

            share_permissions.append(share_permissions_item)

        description = d.pop("description", UNSET)

        dashboard_details = cls(
            name=name,
            share_permissions=share_permissions,
            description=description,
        )

        return dashboard_details
