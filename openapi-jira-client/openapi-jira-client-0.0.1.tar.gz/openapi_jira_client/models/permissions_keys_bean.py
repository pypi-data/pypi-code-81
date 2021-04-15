from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="PermissionsKeysBean")


@attr.s(auto_attribs=True)
class PermissionsKeysBean:
    """  """

    permissions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        permissions = self.permissions

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permissions = cast(List[str], d.pop("permissions"))

        permissions_keys_bean = cls(
            permissions=permissions,
        )

        return permissions_keys_bean
