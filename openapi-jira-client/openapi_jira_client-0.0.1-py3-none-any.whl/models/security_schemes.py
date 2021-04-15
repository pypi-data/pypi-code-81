from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.security_scheme import SecurityScheme
from ..types import UNSET, Unset

T = TypeVar("T", bound="SecuritySchemes")


@attr.s(auto_attribs=True)
class SecuritySchemes:
    """ List of security schemes. """

    issue_security_schemes: Union[Unset, List[SecurityScheme]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue_security_schemes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.issue_security_schemes, Unset):
            issue_security_schemes = []
            for issue_security_schemes_item_data in self.issue_security_schemes:
                issue_security_schemes_item = issue_security_schemes_item_data.to_dict()

                issue_security_schemes.append(issue_security_schemes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issue_security_schemes is not UNSET:
            field_dict["issueSecuritySchemes"] = issue_security_schemes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_security_schemes = []
        _issue_security_schemes = d.pop("issueSecuritySchemes", UNSET)
        for issue_security_schemes_item_data in _issue_security_schemes or []:
            issue_security_schemes_item = SecurityScheme.from_dict(issue_security_schemes_item_data)

            issue_security_schemes.append(issue_security_schemes_item)

        security_schemes = cls(
            issue_security_schemes=issue_security_schemes,
        )

        return security_schemes
