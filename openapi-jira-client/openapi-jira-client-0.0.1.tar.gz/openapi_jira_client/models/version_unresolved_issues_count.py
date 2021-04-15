from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VersionUnresolvedIssuesCount")


@attr.s(auto_attribs=True)
class VersionUnresolvedIssuesCount:
    """ Count of a version's unresolved issues. """

    self_: Union[Unset, str] = UNSET
    issues_unresolved_count: Union[Unset, int] = UNSET
    issues_count: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        issues_unresolved_count = self.issues_unresolved_count
        issues_count = self.issues_count

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if issues_unresolved_count is not UNSET:
            field_dict["issuesUnresolvedCount"] = issues_unresolved_count
        if issues_count is not UNSET:
            field_dict["issuesCount"] = issues_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        issues_unresolved_count = d.pop("issuesUnresolvedCount", UNSET)

        issues_count = d.pop("issuesCount", UNSET)

        version_unresolved_issues_count = cls(
            self_=self_,
            issues_unresolved_count=issues_unresolved_count,
            issues_count=issues_count,
        )

        return version_unresolved_issues_count
