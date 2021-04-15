from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.bulk_operation_error_result import BulkOperationErrorResult
from ..models.created_issue import CreatedIssue
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatedIssues")


@attr.s(auto_attribs=True)
class CreatedIssues:
    """ Details about the issues created and the errors for requests that failed. """

    issues: Union[Unset, List[CreatedIssue]] = UNSET
    errors: Union[Unset, List[BulkOperationErrorResult]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issues: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.issues, Unset):
            issues = []
            for issues_item_data in self.issues:
                issues_item = issues_item_data.to_dict()

                issues.append(issues_item)

        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issues is not UNSET:
            field_dict["issues"] = issues
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issues = []
        _issues = d.pop("issues", UNSET)
        for issues_item_data in _issues or []:
            issues_item = CreatedIssue.from_dict(issues_item_data)

            issues.append(issues_item)

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = BulkOperationErrorResult.from_dict(errors_item_data)

            errors.append(errors_item)

        created_issues = cls(
            issues=issues,
            errors=errors,
        )

        return created_issues
