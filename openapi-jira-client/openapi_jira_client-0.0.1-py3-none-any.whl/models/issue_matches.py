from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.issue_matches_for_jql import IssueMatchesForJQL

T = TypeVar("T", bound="IssueMatches")


@attr.s(auto_attribs=True)
class IssueMatches:
    """ A list of matched issues or errors for each JQL query, in the order the JQL queries were passed. """

    matches: List[IssueMatchesForJQL]

    def to_dict(self) -> Dict[str, Any]:
        matches = []
        for matches_item_data in self.matches:
            matches_item = matches_item_data.to_dict()

            matches.append(matches_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "matches": matches,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        matches = []
        _matches = d.pop("matches")
        for matches_item_data in _matches:
            matches_item = IssueMatchesForJQL.from_dict(matches_item_data)

            matches.append(matches_item)

        issue_matches = cls(
            matches=matches,
        )

        return issue_matches
