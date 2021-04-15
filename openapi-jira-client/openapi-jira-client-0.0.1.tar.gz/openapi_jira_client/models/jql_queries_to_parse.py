from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="JqlQueriesToParse")


@attr.s(auto_attribs=True)
class JqlQueriesToParse:
    """ A list of JQL queries to parse. """

    queries: List[str]

    def to_dict(self) -> Dict[str, Any]:
        queries = self.queries

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
        queries = cast(List[str], d.pop("queries"))

        jql_queries_to_parse = cls(
            queries=queries,
        )

        return jql_queries_to_parse
