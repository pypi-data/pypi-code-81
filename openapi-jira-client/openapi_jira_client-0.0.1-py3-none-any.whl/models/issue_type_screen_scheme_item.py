from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="IssueTypeScreenSchemeItem")


@attr.s(auto_attribs=True)
class IssueTypeScreenSchemeItem:
    """ The screen scheme for an issue type. """

    issue_type_screen_scheme_id: str
    issue_type_id: str
    screen_scheme_id: str

    def to_dict(self) -> Dict[str, Any]:
        issue_type_screen_scheme_id = self.issue_type_screen_scheme_id
        issue_type_id = self.issue_type_id
        screen_scheme_id = self.screen_scheme_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueTypeScreenSchemeId": issue_type_screen_scheme_id,
                "issueTypeId": issue_type_id,
                "screenSchemeId": screen_scheme_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_screen_scheme_id = d.pop("issueTypeScreenSchemeId")

        issue_type_id = d.pop("issueTypeId")

        screen_scheme_id = d.pop("screenSchemeId")

        issue_type_screen_scheme_item = cls(
            issue_type_screen_scheme_id=issue_type_screen_scheme_id,
            issue_type_id=issue_type_id,
            screen_scheme_id=screen_scheme_id,
        )

        return issue_type_screen_scheme_item
