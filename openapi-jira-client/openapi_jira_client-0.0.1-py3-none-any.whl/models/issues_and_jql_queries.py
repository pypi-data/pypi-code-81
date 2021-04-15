from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="IssuesAndJQLQueries")


@attr.s(auto_attribs=True)
class IssuesAndJQLQueries:
    """ List of issues and JQL queries. """

    jqls: List[str]
    issue_ids: List[int]

    def to_dict(self) -> Dict[str, Any]:
        jqls = self.jqls

        issue_ids = self.issue_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "jqls": jqls,
                "issueIds": issue_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        jqls = cast(List[str], d.pop("jqls"))

        issue_ids = cast(List[int], d.pop("issueIds"))

        issues_and_jql_queries = cls(
            jqls=jqls,
            issue_ids=issue_ids,
        )

        return issues_and_jql_queries
