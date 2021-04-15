from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_issue_entity_properties_properties import (
    ComponentsschemasIssueEntityPropertiesProperties,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueEntityProperties")


@attr.s(auto_attribs=True)
class IssueEntityProperties:
    """ Lists of issues and entity properties. See [Entity properties](https://developer.atlassian.com/cloud/jira/platform/jira-entity-properties/) for more information. """

    entities_ids: Union[Unset, List[int]] = UNSET
    properties: Union[Unset, ComponentsschemasIssueEntityPropertiesProperties] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entities_ids: Union[Unset, List[int]] = UNSET
        if not isinstance(self.entities_ids, Unset):
            entities_ids = self.entities_ids

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entities_ids is not UNSET:
            field_dict["entitiesIds"] = entities_ids
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entities_ids = cast(List[int], d.pop("entitiesIds", UNSET))

        properties: Union[Unset, ComponentsschemasIssueEntityPropertiesProperties] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = ComponentsschemasIssueEntityPropertiesProperties.from_dict(_properties)

        issue_entity_properties = cls(
            entities_ids=entities_ids,
            properties=properties,
        )

        return issue_entity_properties
