from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.project_identifier_bean import ProjectIdentifierBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermittedProjects")


@attr.s(auto_attribs=True)
class PermittedProjects:
    """ A list of projects in which a user is granted permissions. """

    projects: Union[Unset, List[ProjectIdentifierBean]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        projects: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.projects, Unset):
            projects = []
            for projects_item_data in self.projects:
                projects_item = projects_item_data.to_dict()

                projects.append(projects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if projects is not UNSET:
            field_dict["projects"] = projects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        projects = []
        _projects = d.pop("projects", UNSET)
        for projects_item_data in _projects or []:
            projects_item = ProjectIdentifierBean.from_dict(projects_item_data)

            projects.append(projects_item)

        permitted_projects = cls(
            projects=projects,
        )

        return permitted_projects
