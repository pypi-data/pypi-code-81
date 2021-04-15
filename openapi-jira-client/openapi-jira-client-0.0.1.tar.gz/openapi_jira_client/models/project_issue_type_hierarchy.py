from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.project_issue_types_hierarchy_level import ProjectIssueTypesHierarchyLevel
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectIssueTypeHierarchy")


@attr.s(auto_attribs=True)
class ProjectIssueTypeHierarchy:
    """ The hierarchy of issue types within a project. """

    project_id: Union[Unset, int] = UNSET
    hierarchy: Union[Unset, List[ProjectIssueTypesHierarchyLevel]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        hierarchy: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.hierarchy, Unset):
            hierarchy = []
            for hierarchy_item_data in self.hierarchy:
                hierarchy_item = hierarchy_item_data.to_dict()

                hierarchy.append(hierarchy_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if hierarchy is not UNSET:
            field_dict["hierarchy"] = hierarchy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("projectId", UNSET)

        hierarchy = []
        _hierarchy = d.pop("hierarchy", UNSET)
        for hierarchy_item_data in _hierarchy or []:
            hierarchy_item = ProjectIssueTypesHierarchyLevel.from_dict(hierarchy_item_data)

            hierarchy.append(hierarchy_item)

        project_issue_type_hierarchy = cls(
            project_id=project_id,
            hierarchy=hierarchy,
        )

        return project_issue_type_hierarchy
