from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.simple_error_collection import SimpleErrorCollection
from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoveOptionFromIssuesResult")


@attr.s(auto_attribs=True)
class RemoveOptionFromIssuesResult:
    """  """

    modified_issues: Union[Unset, List[int]] = UNSET
    unmodified_issues: Union[Unset, List[int]] = UNSET
    errors: Union[Unset, SimpleErrorCollection] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        modified_issues: Union[Unset, List[int]] = UNSET
        if not isinstance(self.modified_issues, Unset):
            modified_issues = self.modified_issues

        unmodified_issues: Union[Unset, List[int]] = UNSET
        if not isinstance(self.unmodified_issues, Unset):
            unmodified_issues = self.unmodified_issues

        errors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if modified_issues is not UNSET:
            field_dict["modifiedIssues"] = modified_issues
        if unmodified_issues is not UNSET:
            field_dict["unmodifiedIssues"] = unmodified_issues
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        modified_issues = cast(List[int], d.pop("modifiedIssues", UNSET))

        unmodified_issues = cast(List[int], d.pop("unmodifiedIssues", UNSET))

        errors: Union[Unset, SimpleErrorCollection] = UNSET
        _errors = d.pop("errors", UNSET)
        if not isinstance(_errors, Unset):
            errors = SimpleErrorCollection.from_dict(_errors)

        remove_option_from_issues_result = cls(
            modified_issues=modified_issues,
            unmodified_issues=unmodified_issues,
            errors=errors,
        )

        return remove_option_from_issues_result
