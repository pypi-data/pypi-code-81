from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.parsed_jql_query import ParsedJqlQuery

T = TypeVar("T", bound="ParsedJqlQueries")


@attr.s(auto_attribs=True)
class ParsedJqlQueries:
    """ A list of parsed JQL queries. """

    queries: List[ParsedJqlQuery]

    def to_dict(self) -> Dict[str, Any]:
        queries = []
        for queries_item_data in self.queries:
            queries_item = queries_item_data.to_dict()

            queries.append(queries_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "queries": queries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        queries = []
        _queries = d.pop("queries")
        for queries_item_data in _queries:
            queries_item = ParsedJqlQuery.from_dict(queries_item_data)

            queries.append(queries_item)

        parsed_jql_queries = cls(
            queries=queries,
        )

        return parsed_jql_queries
