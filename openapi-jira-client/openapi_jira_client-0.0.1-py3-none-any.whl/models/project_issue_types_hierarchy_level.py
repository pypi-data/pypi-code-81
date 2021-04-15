from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.issue_type_info import IssueTypeInfo
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectIssueTypesHierarchyLevel")


@attr.s(auto_attribs=True)
class ProjectIssueTypesHierarchyLevel:
    """ Details of an issue type hierarchy level. """

    entity_id: Union[Unset, str] = UNSET
    level: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    issue_types: Union[Unset, List[IssueTypeInfo]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entity_id = self.entity_id
        level = self.level
        name = self.name
        issue_types: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.issue_types, Unset):
            issue_types = []
            for issue_types_item_data in self.issue_types:
                issue_types_item = issue_types_item_data.to_dict()

                issue_types.append(issue_types_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if level is not UNSET:
            field_dict["level"] = level
        if name is not UNSET:
            field_dict["name"] = name
        if issue_types is not UNSET:
            field_dict["issueTypes"] = issue_types

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_id = d.pop("entityId", UNSET)

        level = d.pop("level", UNSET)

        name = d.pop("name", UNSET)

        issue_types = []
        _issue_types = d.pop("issueTypes", UNSET)
        for issue_types_item_data in _issue_types or []:
            issue_types_item = IssueTypeInfo.from_dict(issue_types_item_data)

            issue_types.append(issue_types_item)

        project_issue_types_hierarchy_level = cls(
            entity_id=entity_id,
            level=level,
            name=name,
            issue_types=issue_types,
        )

        return project_issue_types_hierarchy_level
