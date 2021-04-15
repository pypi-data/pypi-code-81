from typing import Any, Dict, Type, TypeVar

import attr

from ..models.permission_holder import PermissionHolder

T = TypeVar("T", bound="IssueSecurityLevelMember")


@attr.s(auto_attribs=True)
class IssueSecurityLevelMember:
    """ Issue security level member. """

    id_: int
    issue_security_level_id: int
    holder: PermissionHolder

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        issue_security_level_id = self.issue_security_level_id
        holder = self.holder.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "issueSecurityLevelId": issue_security_level_id,
                "holder": holder,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        issue_security_level_id = d.pop("issueSecurityLevelId")

        holder = PermissionHolder.from_dict(d.pop("holder"))

        issue_security_level_member = cls(
            id_=id_,
            issue_security_level_id=issue_security_level_id,
            holder=holder,
        )

        return issue_security_level_member
