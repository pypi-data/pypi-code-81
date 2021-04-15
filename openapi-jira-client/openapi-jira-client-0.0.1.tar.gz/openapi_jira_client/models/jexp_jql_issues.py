from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_jexp_jql_issues_validation import ComponentsschemasJexpJqlIssuesValidation
from ..types import UNSET, Unset

T = TypeVar("T", bound="JexpJqlIssues")


@attr.s(auto_attribs=True)
class JexpJqlIssues:
    """ The JQL specifying the issues available in the evaluated Jira expression under the `issues` context variable. Not all issues returned by the JQL query are loaded, only those described by the `startAt` and `maxResults` properties. To determine whether it is necessary to iterate to ensure all the issues returned by the JQL query are evaluated, inspect `meta.issues.jql.count` in the response. """

    query: Union[Unset, str] = UNSET
    start_at: Union[Unset, int] = UNSET
    max_results: Union[Unset, int] = UNSET
    validation: Union[Unset, ComponentsschemasJexpJqlIssuesValidation] = ComponentsschemasJexpJqlIssuesValidation.STRICT

    def to_dict(self) -> Dict[str, Any]:
        query = self.query
        start_at = self.start_at
        max_results = self.max_results
        validation: Union[Unset, str] = UNSET
        if not isinstance(self.validation, Unset):
            validation = self.validation.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if query is not UNSET:
            field_dict["query"] = query
        if start_at is not UNSET:
            field_dict["startAt"] = start_at
        if max_results is not UNSET:
            field_dict["maxResults"] = max_results
        if validation is not UNSET:
            field_dict["validation"] = validation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query = d.pop("query", UNSET)

        start_at = d.pop("startAt", UNSET)

        max_results = d.pop("maxResults", UNSET)

        validation: Union[Unset, ComponentsschemasJexpJqlIssuesValidation] = UNSET
        _validation = d.pop("validation", UNSET)
        if not isinstance(_validation, Unset):
            validation = ComponentsschemasJexpJqlIssuesValidation(_validation)

        jexp_jql_issues = cls(
            query=query,
            start_at=start_at,
            max_results=max_results,
            validation=validation,
        )

        return jexp_jql_issues
