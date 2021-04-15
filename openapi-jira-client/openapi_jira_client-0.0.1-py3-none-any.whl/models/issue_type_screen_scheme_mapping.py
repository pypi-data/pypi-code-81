from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="IssueTypeScreenSchemeMapping")


@attr.s(auto_attribs=True)
class IssueTypeScreenSchemeMapping:
    """ The IDs of the screen schemes for the issue type IDs. """

    issue_type_id: str
    screen_scheme_id: str

    def to_dict(self) -> Dict[str, Any]:
        issue_type_id = self.issue_type_id
        screen_scheme_id = self.screen_scheme_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueTypeId": issue_type_id,
                "screenSchemeId": screen_scheme_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_id = d.pop("issueTypeId")

        screen_scheme_id = d.pop("screenSchemeId")

        issue_type_screen_scheme_mapping = cls(
            issue_type_id=issue_type_id,
            screen_scheme_id=screen_scheme_id,
        )

        return issue_type_screen_scheme_mapping
