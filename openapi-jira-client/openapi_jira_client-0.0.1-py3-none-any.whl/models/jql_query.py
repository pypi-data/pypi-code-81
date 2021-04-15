from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.jql_query_clause import JqlQueryClause
from ..models.jql_query_order_by_clause import JqlQueryOrderByClause
from ..types import UNSET, Unset

T = TypeVar("T", bound="JqlQuery")


@attr.s(auto_attribs=True)
class JqlQuery:
    """ A parsed JQL query. """

    where: Union[Unset, JqlQueryClause] = UNSET
    order_by: Union[Unset, JqlQueryOrderByClause] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        where: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.where, Unset):
            where = self.where.to_dict()

        order_by: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.order_by, Unset):
            order_by = self.order_by.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if where is not UNSET:
            field_dict["where"] = where
        if order_by is not UNSET:
            field_dict["orderBy"] = order_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        where: Union[Unset, JqlQueryClause] = UNSET
        _where = d.pop("where", UNSET)
        if not isinstance(_where, Unset):
            where = JqlQueryClause.from_dict(_where)

        order_by: Union[Unset, JqlQueryOrderByClause] = UNSET
        _order_by = d.pop("orderBy", UNSET)
        if not isinstance(_order_by, Unset):
            order_by = JqlQueryOrderByClause.from_dict(_order_by)

        jql_query = cls(
            where=where,
            order_by=order_by,
        )

        return jql_query
