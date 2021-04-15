from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectEmailAddress")


@attr.s(auto_attribs=True)
class ProjectEmailAddress:
    """ A project's sender email address. """

    email_address: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        email_address = self.email_address

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email_address = d.pop("emailAddress", UNSET)

        project_email_address = cls(
            email_address=email_address,
        )

        return project_email_address
