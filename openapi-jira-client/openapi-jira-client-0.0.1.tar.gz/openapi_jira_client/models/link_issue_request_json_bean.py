from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.comment import Comment
from ..models.issue_link_type import IssueLinkType
from ..models.linked_issue import LinkedIssue
from ..types import UNSET, Unset

T = TypeVar("T", bound="LinkIssueRequestJsonBean")


@attr.s(auto_attribs=True)
class LinkIssueRequestJsonBean:
    """  """

    type_: IssueLinkType
    inward_issue: LinkedIssue
    outward_issue: LinkedIssue
    comment: Union[Unset, Comment] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type_ = self.type_.to_dict()

        inward_issue = self.inward_issue.to_dict()

        outward_issue = self.outward_issue.to_dict()

        comment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.comment, Unset):
            comment = self.comment.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type_,
                "inwardIssue": inward_issue,
                "outwardIssue": outward_issue,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = IssueLinkType.from_dict(d.pop("type"))

        inward_issue = LinkedIssue.from_dict(d.pop("inwardIssue"))

        outward_issue = LinkedIssue.from_dict(d.pop("outwardIssue"))

        comment: Union[Unset, Comment] = UNSET
        _comment = d.pop("comment", UNSET)
        if not isinstance(_comment, Unset):
            comment = Comment.from_dict(_comment)

        link_issue_request_json_bean = cls(
            type_=type_,
            inward_issue=inward_issue,
            outward_issue=outward_issue,
            comment=comment,
        )

        return link_issue_request_json_bean
