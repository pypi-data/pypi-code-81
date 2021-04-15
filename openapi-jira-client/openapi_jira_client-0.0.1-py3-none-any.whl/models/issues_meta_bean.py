from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.issues_jql_meta_data_bean import IssuesJqlMetaDataBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssuesMetaBean")


@attr.s(auto_attribs=True)
class IssuesMetaBean:
    """ Meta data describing the `issues` context variable. """

    jql: Union[Unset, IssuesJqlMetaDataBean] = UNSET

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
        jql: Union[Unset, IssuesJqlMetaDataBean] = UNSET
        _jql = d.pop("jql", UNSET)
        if not isinstance(_jql, Unset):
            jql = IssuesJqlMetaDataBean.from_dict(_jql)

        issues_meta_bean = cls(
            jql=jql,
        )

        return issues_meta_bean
