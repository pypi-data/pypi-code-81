from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="WarehouseCredentials")


@attr.s(auto_attribs=True)
class WarehouseCredentials:
    """  """

    expires_at: str
    password: str
    username: str

    def to_dict(self) -> Dict[str, Any]:
        expires_at = self.expires_at
        password = self.password
        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expiresAt": expires_at,
                "password": password,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expires_at = d.pop("expiresAt")

        password = d.pop("password")

        username = d.pop("username")

        warehouse_credentials = cls(
            expires_at=expires_at,
            password=password,
            username=username,
        )

        return warehouse_credentials
