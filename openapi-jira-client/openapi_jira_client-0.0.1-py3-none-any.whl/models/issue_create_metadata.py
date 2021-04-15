from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.project_issue_create_metadata import ProjectIssueCreateMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueCreateMetadata")


@attr.s(auto_attribs=True)
class IssueCreateMetadata:
    """ The wrapper for the issue creation metadata for a list of projects. """

    expand: Union[Unset, str] = UNSET
    projects: Union[Unset, List[ProjectIssueCreateMetadata]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        projects: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.projects, Unset):
            projects = []
            for projects_item_data in self.projects:
                projects_item = projects_item_data.to_dict()

                projects.append(projects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if projects is not UNSET:
            field_dict["projects"] = projects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        projects = []
        _projects = d.pop("projects", UNSET)
        for projects_item_data in _projects or []:
            projects_item = ProjectIssueCreateMetadata.from_dict(projects_item_data)

            projects.append(projects_item)

        issue_create_metadata = cls(
            expand=expand,
            projects=projects,
        )

        return issue_create_metadata
