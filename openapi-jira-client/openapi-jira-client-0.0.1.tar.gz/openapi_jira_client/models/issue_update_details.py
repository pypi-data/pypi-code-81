from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.componentsschemas_issue_update_details_fields import ComponentsschemasIssueUpdateDetailsFields
from ..models.componentsschemas_issue_update_details_update import ComponentsschemasIssueUpdateDetailsUpdate
from ..models.entity_property import EntityProperty
from ..models.history_metadata import HistoryMetadata
from ..models.issue_transition import IssueTransition
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueUpdateDetails")


@attr.s(auto_attribs=True)
class IssueUpdateDetails:
    """ Details of an issue update request. """

    transition: Union[Unset, IssueTransition] = UNSET
    fields: Union[Unset, ComponentsschemasIssueUpdateDetailsFields] = UNSET
    update: Union[Unset, ComponentsschemasIssueUpdateDetailsUpdate] = UNSET
    history_metadata: Union[Unset, HistoryMetadata] = UNSET
    properties: Union[Unset, List[EntityProperty]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        transition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.transition, Unset):
            transition = self.transition.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        update: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.update, Unset):
            update = self.update.to_dict()

        history_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.history_metadata, Unset):
            history_metadata = self.history_metadata.to_dict()

        properties: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = []
            for properties_item_data in self.properties:
                properties_item = properties_item_data.to_dict()

                properties.append(properties_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if transition is not UNSET:
            field_dict["transition"] = transition
        if fields is not UNSET:
            field_dict["fields"] = fields
        if update is not UNSET:
            field_dict["update"] = update
        if history_metadata is not UNSET:
            field_dict["historyMetadata"] = history_metadata
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        transition: Union[Unset, IssueTransition] = UNSET
        _transition = d.pop("transition", UNSET)
        if not isinstance(_transition, Unset):
            transition = IssueTransition.from_dict(_transition)

        fields: Union[Unset, ComponentsschemasIssueUpdateDetailsFields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = ComponentsschemasIssueUpdateDetailsFields.from_dict(_fields)

        update: Union[Unset, ComponentsschemasIssueUpdateDetailsUpdate] = UNSET
        _update = d.pop("update", UNSET)
        if not isinstance(_update, Unset):
            update = ComponentsschemasIssueUpdateDetailsUpdate.from_dict(_update)

        history_metadata: Union[Unset, HistoryMetadata] = UNSET
        _history_metadata = d.pop("historyMetadata", UNSET)
        if not isinstance(_history_metadata, Unset):
            history_metadata = HistoryMetadata.from_dict(_history_metadata)

        properties = []
        _properties = d.pop("properties", UNSET)
        for properties_item_data in _properties or []:
            properties_item = EntityProperty.from_dict(properties_item_data)

            properties.append(properties_item)

        issue_update_details = cls(
            transition=transition,
            fields=fields,
            update=update,
            history_metadata=history_metadata,
            properties=properties,
        )

        issue_update_details.additional_properties = d
        return issue_update_details

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
