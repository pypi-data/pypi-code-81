from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.issue_type_scheme import IssueTypeScheme

T = TypeVar("T", bound="IssueTypeSchemeProjects")


@attr.s(auto_attribs=True)
class IssueTypeSchemeProjects:
    """ Issue type scheme with a list of the projects that use it. """

    issue_type_scheme: IssueTypeScheme
    project_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        issue_type_scheme = self.issue_type_scheme.to_dict()

        project_ids = self.project_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueTypeScheme": issue_type_scheme,
                "projectIds": project_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_scheme = IssueTypeScheme.from_dict(d.pop("issueTypeScheme"))

        project_ids = cast(List[str], d.pop("projectIds"))

        issue_type_scheme_projects = cls(
            issue_type_scheme=issue_type_scheme,
            project_ids=project_ids,
        )

        return issue_type_scheme_projects
