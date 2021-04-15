from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.jexp_jql_issues import JexpJqlIssues
from ..types import UNSET, Unset

T = TypeVar("T", bound="JexpIssues")


@attr.s(auto_attribs=True)
class JexpIssues:
    """ The JQL specifying the issues available in the evaluated Jira expression under the `issues` context variable. """

    jql: Union[Unset, JexpJqlIssues] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        jql: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.jql, Unset):
            jql = self.jql.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if jql is not UNSET:
            field_dict["jql"] = jql

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        jql: Union[Unset, JexpJqlIssues] = UNSET
        _jql = d.pop("jql", UNSET)
        if not isinstance(_jql, Unset):
            jql = JexpJqlIssues.from_dict(_jql)

        jexp_issues = cls(
            jql=jql,
        )

        return jexp_issues
