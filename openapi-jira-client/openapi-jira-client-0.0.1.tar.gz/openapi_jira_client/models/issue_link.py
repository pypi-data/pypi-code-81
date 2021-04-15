from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.issue_link_type import IssueLinkType
from ..models.linked_issue import LinkedIssue
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueLink")


@attr.s(auto_attribs=True)
class IssueLink:
    """ Details of a link between issues. """

    type_: IssueLinkType
    inward_issue: LinkedIssue
    outward_issue: LinkedIssue
    id_: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type_ = self.type_.to_dict()

        inward_issue = self.inward_issue.to_dict()

        outward_issue = self.outward_issue.to_dict()

        id_ = self.id_
        self_ = self.self_

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type_,
                "inwardIssue": inward_issue,
                "outwardIssue": outward_issue,
            }
        )
        if id_ is not UNSET:
            field_dict["id"] = id_
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = IssueLinkType.from_dict(d.pop("type"))

        inward_issue = LinkedIssue.from_dict(d.pop("inwardIssue"))

        outward_issue = LinkedIssue.from_dict(d.pop("outwardIssue"))

        id_ = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        issue_link = cls(
            type_=type_,
            inward_issue=inward_issue,
            outward_issue=outward_issue,
            id_=id_,
            self_=self_,
        )

        return issue_link
