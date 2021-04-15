from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_search_request_bean_validate_query import (
    ComponentsschemasSearchRequestBeanValidateQuery,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchRequestBean")


@attr.s(auto_attribs=True)
class SearchRequestBean:
    """  """

    jql: Union[Unset, str] = UNSET
    start_at: Union[Unset, int] = UNSET
    max_results: Union[Unset, int] = 50
    fields: Union[Unset, List[str]] = UNSET
    validate_query: Union[Unset, ComponentsschemasSearchRequestBeanValidateQuery] = UNSET
    expand: Union[Unset, List[str]] = UNSET
    properties: Union[Unset, List[str]] = UNSET
    fields_by_keys: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        jql = self.jql
        start_at = self.start_at
        max_results = self.max_results
        fields: Union[Unset, List[str]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields

        validate_query: Union[Unset, str] = UNSET
        if not isinstance(self.validate_query, Unset):
            validate_query = self.validate_query.value

        expand: Union[Unset, List[str]] = UNSET
        if not isinstance(self.expand, Unset):
            expand = self.expand

        properties: Union[Unset, List[str]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties

        fields_by_keys = self.fields_by_keys

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if jql is not UNSET:
            field_dict["jql"] = jql
        if start_at is not UNSET:
            field_dict["startAt"] = start_at
        if max_results is not UNSET:
            field_dict["maxResults"] = max_results
        if fields is not UNSET:
            field_dict["fields"] = fields
        if validate_query is not UNSET:
            field_dict["validateQuery"] = validate_query
        if expand is not UNSET:
            field_dict["expand"] = expand
        if properties is not UNSET:
            field_dict["properties"] = properties
        if fields_by_keys is not UNSET:
            field_dict["fieldsByKeys"] = fields_by_keys

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        jql = d.pop("jql", UNSET)

        start_at = d.pop("startAt", UNSET)

        max_results = d.pop("maxResults", UNSET)

        fields = cast(List[str], d.pop("fields", UNSET))

        validate_query: Union[Unset, ComponentsschemasSearchRequestBeanValidateQuery] = UNSET
        _validate_query = d.pop("validateQuery", UNSET)
        if not isinstance(_validate_query, Unset):
            validate_query = ComponentsschemasSearchRequestBeanValidateQuery(_validate_query)

        expand = cast(List[str], d.pop("expand", UNSET))

        properties = cast(List[str], d.pop("properties", UNSET))

        fields_by_keys = d.pop("fieldsByKeys", UNSET)

        search_request_bean = cls(
            jql=jql,
            start_at=start_at,
            max_results=max_results,
            fields=fields,
            validate_query=validate_query,
            expand=expand,
            properties=properties,
            fields_by_keys=fields_by_keys,
        )

        return search_request_bean
