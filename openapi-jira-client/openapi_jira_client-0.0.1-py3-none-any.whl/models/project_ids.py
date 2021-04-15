from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="ProjectIds")


@attr.s(auto_attribs=True)
class ProjectIds:
    """ A list of project IDs. """

    project_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        project_ids = self.project_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectIds": project_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_ids = cast(List[str], d.pop("projectIds"))

        project_ids = cls(
            project_ids=project_ids,
        )

        return project_ids
