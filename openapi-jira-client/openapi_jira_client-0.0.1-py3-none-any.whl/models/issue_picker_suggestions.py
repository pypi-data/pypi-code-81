from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.issue_picker_suggestions_issue_type import IssuePickerSuggestionsIssueType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssuePickerSuggestions")


@attr.s(auto_attribs=True)
class IssuePickerSuggestions:
    """ A list of issues suggested for use in auto-completion. """

    sections: Union[Unset, List[IssuePickerSuggestionsIssueType]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        sections: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sections, Unset):
            sections = []
            for sections_item_data in self.sections:
                sections_item = sections_item_data.to_dict()

                sections.append(sections_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if sections is not UNSET:
            field_dict["sections"] = sections

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sections = []
        _sections = d.pop("sections", UNSET)
        for sections_item_data in _sections or []:
            sections_item = IssuePickerSuggestionsIssueType.from_dict(sections_item_data)

            sections.append(sections_item)

        issue_picker_suggestions = cls(
            sections=sections,
        )

        return issue_picker_suggestions
