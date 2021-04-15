from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserWriteBean")


@attr.s(auto_attribs=True)
class UserWriteBean:
    """  """

    email_address: str
    display_name: str
    self_: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    application_keys: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email_address = self.email_address
        display_name = self.display_name
        self_ = self.self_
        key = self.key
        name = self.name
        password = self.password
        application_keys: Union[Unset, List[str]] = UNSET
        if not isinstance(self.application_keys, Unset):
            application_keys = self.application_keys

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "emailAddress": email_address,
                "displayName": display_name,
            }
        )
        if self_ is not UNSET:
            field_dict["self"] = self_
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if password is not UNSET:
            field_dict["password"] = password
        if application_keys is not UNSET:
            field_dict["applicationKeys"] = application_keys

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email_address = d.pop("emailAddress")

        display_name = d.pop("displayName")

        self_ = d.pop("self", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        password = d.pop("password", UNSET)

        application_keys = cast(List[str], d.pop("applicationKeys", UNSET))

        user_write_bean = cls(
            email_address=email_address,
            display_name=display_name,
            self_=self_,
            key=key,
            name=name,
            password=password,
            application_keys=application_keys,
        )

        user_write_bean.additional_properties = d
        return user_write_bean

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
