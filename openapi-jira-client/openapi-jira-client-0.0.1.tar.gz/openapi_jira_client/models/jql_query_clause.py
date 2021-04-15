from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="JqlQueryClause")


@attr.s(auto_attribs=True)
class JqlQueryClause:
    """ A JQL query clause. """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        src_dict.copy()
        jql_query_clause = cls()

        return jql_query_clause
