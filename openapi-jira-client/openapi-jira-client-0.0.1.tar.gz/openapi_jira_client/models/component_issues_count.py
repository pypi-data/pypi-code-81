from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentIssuesCount")


@attr.s(auto_attribs=True)
class ComponentIssuesCount:
    """ Count of issues assigned to a component. """

    self_: Union[Unset, str] = UNSET
    issue_count: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        issue_count = self.issue_count

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if issue_count is not UNSET:
            field_dict["issueCount"] = issue_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        issue_count = d.pop("issueCount", UNSET)

        component_issues_count = cls(
            self_=self_,
            issue_count=issue_count,
        )

        return component_issues_count
