from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeScreenSchemeProjectAssociation")


@attr.s(auto_attribs=True)
class IssueTypeScreenSchemeProjectAssociation:
    """ Associated issue type screen scheme and project. """

    issue_type_screen_scheme_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue_type_screen_scheme_id = self.issue_type_screen_scheme_id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issue_type_screen_scheme_id is not UNSET:
            field_dict["issueTypeScreenSchemeId"] = issue_type_screen_scheme_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_screen_scheme_id = d.pop("issueTypeScreenSchemeId", UNSET)

        project_id = d.pop("projectId", UNSET)

        issue_type_screen_scheme_project_association = cls(
            issue_type_screen_scheme_id=issue_type_screen_scheme_id,
            project_id=project_id,
        )

        return issue_type_screen_scheme_project_association
