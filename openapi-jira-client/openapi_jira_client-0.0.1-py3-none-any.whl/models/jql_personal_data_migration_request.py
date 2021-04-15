from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="JQLPersonalDataMigrationRequest")


@attr.s(auto_attribs=True)
class JQLPersonalDataMigrationRequest:
    """ The JQL queries to be converted. """

    query_strings: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        query_strings: Union[Unset, List[str]] = UNSET
        if not isinstance(self.query_strings, Unset):
            query_strings = self.query_strings

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if query_strings is not UNSET:
            field_dict["queryStrings"] = query_strings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_strings = cast(List[str], d.pop("queryStrings", UNSET))

        jql_personal_data_migration_request = cls(
            query_strings=query_strings,
        )

        return jql_personal_data_migration_request
