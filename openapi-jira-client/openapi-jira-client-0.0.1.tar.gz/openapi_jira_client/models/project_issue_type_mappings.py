from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.project_issue_type_mapping import ProjectIssueTypeMapping

T = TypeVar("T", bound="ProjectIssueTypeMappings")


@attr.s(auto_attribs=True)
class ProjectIssueTypeMappings:
    """ The project and issue type mappings. """

    mappings: List[ProjectIssueTypeMapping]

    def to_dict(self) -> Dict[str, Any]:
        mappings = []
        for mappings_item_data in self.mappings:
            mappings_item = mappings_item_data.to_dict()

            mappings.append(mappings_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "mappings": mappings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mappings = []
        _mappings = d.pop("mappings")
        for mappings_item_data in _mappings:
            mappings_item = ProjectIssueTypeMapping.from_dict(mappings_item_data)

            mappings.append(mappings_item)

        project_issue_type_mappings = cls(
            mappings=mappings,
        )

        return project_issue_type_mappings
