from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entity_property import EntityProperty
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangedWorklog")


@attr.s(auto_attribs=True)
class ChangedWorklog:
    """ Details of a changed worklog. """

    worklog_id: Union[Unset, int] = UNSET
    updated_time: Union[Unset, int] = UNSET
    properties: Union[Unset, List[EntityProperty]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        worklog_id = self.worklog_id
        updated_time = self.updated_time
        properties: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = []
            for properties_item_data in self.properties:
                properties_item = properties_item_data.to_dict()

                properties.append(properties_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if worklog_id is not UNSET:
            field_dict["worklogId"] = worklog_id
        if updated_time is not UNSET:
            field_dict["updatedTime"] = updated_time
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        worklog_id = d.pop("worklogId", UNSET)

        updated_time = d.pop("updatedTime", UNSET)

        properties = []
        _properties = d.pop("properties", UNSET)
        for properties_item_data in _properties or []:
            properties_item = EntityProperty.from_dict(properties_item_data)

            properties.append(properties_item)

        changed_worklog = cls(
            worklog_id=worklog_id,
            updated_time=updated_time,
            properties=properties,
        )

        return changed_worklog
