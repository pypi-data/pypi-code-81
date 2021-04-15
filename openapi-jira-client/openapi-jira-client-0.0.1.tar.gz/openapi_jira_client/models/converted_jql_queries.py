from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.jql_query_with_unknown_users import JQLQueryWithUnknownUsers
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConvertedJQLQueries")


@attr.s(auto_attribs=True)
class ConvertedJQLQueries:
    """ The converted JQL queries. """

    query_strings: Union[Unset, List[str]] = UNSET
    queries_with_unknown_users: Union[Unset, List[JQLQueryWithUnknownUsers]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        query_strings: Union[Unset, List[str]] = UNSET
        if not isinstance(self.query_strings, Unset):
            query_strings = self.query_strings

        queries_with_unknown_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.queries_with_unknown_users, Unset):
            queries_with_unknown_users = []
            for queries_with_unknown_users_item_data in self.queries_with_unknown_users:
                queries_with_unknown_users_item = queries_with_unknown_users_item_data.to_dict()

                queries_with_unknown_users.append(queries_with_unknown_users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if query_strings is not UNSET:
            field_dict["queryStrings"] = query_strings
        if queries_with_unknown_users is not UNSET:
            field_dict["queriesWithUnknownUsers"] = queries_with_unknown_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_strings = cast(List[str], d.pop("queryStrings", UNSET))

        queries_with_unknown_users = []
        _queries_with_unknown_users = d.pop("queriesWithUnknownUsers", UNSET)
        for queries_with_unknown_users_item_data in _queries_with_unknown_users or []:
            queries_with_unknown_users_item = JQLQueryWithUnknownUsers.from_dict(queries_with_unknown_users_item_data)

            queries_with_unknown_users.append(queries_with_unknown_users_item)

        converted_jql_queries = cls(
            query_strings=query_strings,
            queries_with_unknown_users=queries_with_unknown_users,
        )

        return converted_jql_queries
