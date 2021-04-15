from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="JQLQueryWithUnknownUsers")


@attr.s(auto_attribs=True)
class JQLQueryWithUnknownUsers:
    """ JQL queries that contained users that could not be found """

    original_query: Union[Unset, str] = UNSET
    converted_query: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        original_query = self.original_query
        converted_query = self.converted_query

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if original_query is not UNSET:
            field_dict["originalQuery"] = original_query
        if converted_query is not UNSET:
            field_dict["convertedQuery"] = converted_query

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        original_query = d.pop("originalQuery", UNSET)

        converted_query = d.pop("convertedQuery", UNSET)

        jql_query_with_unknown_users = cls(
            original_query=original_query,
            converted_query=converted_query,
        )

        return jql_query_with_unknown_users
