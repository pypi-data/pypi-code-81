from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeToContextMapping")


@attr.s(auto_attribs=True)
class IssueTypeToContextMapping:
    """ Mapping of an issue type to a context. """

    context_id: str
    issue_type_id: Union[Unset, str] = UNSET
    is_any_issue_type: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        context_id = self.context_id
        issue_type_id = self.issue_type_id
        is_any_issue_type = self.is_any_issue_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "contextId": context_id,
            }
        )
        if issue_type_id is not UNSET:
            field_dict["issueTypeId"] = issue_type_id
        if is_any_issue_type is not UNSET:
            field_dict["isAnyIssueType"] = is_any_issue_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        context_id = d.pop("contextId")

        issue_type_id = d.pop("issueTypeId", UNSET)

        is_any_issue_type = d.pop("isAnyIssueType", UNSET)

        issue_type_to_context_mapping = cls(
            context_id=context_id,
            issue_type_id=issue_type_id,
            is_any_issue_type=is_any_issue_type,
        )

        return issue_type_to_context_mapping
