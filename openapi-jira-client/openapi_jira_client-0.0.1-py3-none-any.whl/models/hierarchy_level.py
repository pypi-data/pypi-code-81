from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_hierarchy_level_global_hierarchy_level import (
    ComponentsschemasHierarchyLevelGlobalHierarchyLevel,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="HierarchyLevel")


@attr.s(auto_attribs=True)
class HierarchyLevel:
    """  """

    id_: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    above_level_id: Union[Unset, int] = UNSET
    below_level_id: Union[Unset, int] = UNSET
    project_configuration_id: Union[Unset, int] = UNSET
    level: Union[Unset, int] = UNSET
    issue_type_ids: Union[Unset, List[int]] = UNSET
    external_uuid: Union[Unset, str] = UNSET
    global_hierarchy_level: Union[Unset, ComponentsschemasHierarchyLevelGlobalHierarchyLevel] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        above_level_id = self.above_level_id
        below_level_id = self.below_level_id
        project_configuration_id = self.project_configuration_id
        level = self.level
        issue_type_ids: Union[Unset, List[int]] = UNSET
        if not isinstance(self.issue_type_ids, Unset):
            issue_type_ids = self.issue_type_ids

        external_uuid = self.external_uuid
        global_hierarchy_level: Union[Unset, str] = UNSET
        if not isinstance(self.global_hierarchy_level, Unset):
            global_hierarchy_level = self.global_hierarchy_level.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if above_level_id is not UNSET:
            field_dict["aboveLevelId"] = above_level_id
        if below_level_id is not UNSET:
            field_dict["belowLevelId"] = below_level_id
        if project_configuration_id is not UNSET:
            field_dict["projectConfigurationId"] = project_configuration_id
        if level is not UNSET:
            field_dict["level"] = level
        if issue_type_ids is not UNSET:
            field_dict["issueTypeIds"] = issue_type_ids
        if external_uuid is not UNSET:
            field_dict["externalUuid"] = external_uuid
        if global_hierarchy_level is not UNSET:
            field_dict["globalHierarchyLevel"] = global_hierarchy_level

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        above_level_id = d.pop("aboveLevelId", UNSET)

        below_level_id = d.pop("belowLevelId", UNSET)

        project_configuration_id = d.pop("projectConfigurationId", UNSET)

        level = d.pop("level", UNSET)

        issue_type_ids = cast(List[int], d.pop("issueTypeIds", UNSET))

        external_uuid = d.pop("externalUuid", UNSET)

        global_hierarchy_level: Union[Unset, ComponentsschemasHierarchyLevelGlobalHierarchyLevel] = UNSET
        _global_hierarchy_level = d.pop("globalHierarchyLevel", UNSET)
        if not isinstance(_global_hierarchy_level, Unset):
            global_hierarchy_level = ComponentsschemasHierarchyLevelGlobalHierarchyLevel(_global_hierarchy_level)

        hierarchy_level = cls(
            id_=id_,
            name=name,
            above_level_id=above_level_id,
            below_level_id=below_level_id,
            project_configuration_id=project_configuration_id,
            level=level,
            issue_type_ids=issue_type_ids,
            external_uuid=external_uuid,
            global_hierarchy_level=global_hierarchy_level,
        )

        return hierarchy_level
