from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="IssueMatchesForJQL")


@attr.s(auto_attribs=True)
class IssueMatchesForJQL:
    """ A list of the issues matched to a JQL query or details of errors encountered during matching. """

    matched_issues: List[int]
    errors: List[str]

    def to_dict(self) -> Dict[str, Any]:
        matched_issues = self.matched_issues

        errors = self.errors

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "matchedIssues": matched_issues,
                "errors": errors,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        matched_issues = cast(List[int], d.pop("matchedIssues"))

        errors = cast(List[str], d.pop("errors"))

        issue_matches_for_jql = cls(
            matched_issues=matched_issues,
            errors=errors,
        )

        return issue_matches_for_jql
