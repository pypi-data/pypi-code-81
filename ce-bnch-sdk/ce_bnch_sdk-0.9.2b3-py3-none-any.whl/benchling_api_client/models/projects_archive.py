from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.projects_archive_reason import ProjectsArchiveReason

T = TypeVar("T", bound="ProjectsArchive")


@attr.s(auto_attribs=True)
class ProjectsArchive:
    """  """

    project_ids: List[str]
    reason: ProjectsArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        project_ids = self.project_ids

        reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectIds": project_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_ids = cast(List[str], d.pop("projectIds"))

        reason = ProjectsArchiveReason(d.pop("reason"))

        projects_archive = cls(
            project_ids=project_ids,
            reason=reason,
        )

        return projects_archive
