from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_issue_field_option_properties import ComponentsschemasIssueFieldOptionProperties
from ..models.issue_field_option_configuration import IssueFieldOptionConfiguration
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueFieldOption")


@attr.s(auto_attribs=True)
class IssueFieldOption:
    """ Details of the options for a select list issue field. """

    id_: int
    value: str
    properties: Union[Unset, ComponentsschemasIssueFieldOptionProperties] = UNSET
    config: Union[Unset, IssueFieldOptionConfiguration] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        value = self.value
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "value": value,
            }
        )
        if properties is not UNSET:
            field_dict["properties"] = properties
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        value = d.pop("value")

        properties: Union[Unset, ComponentsschemasIssueFieldOptionProperties] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = ComponentsschemasIssueFieldOptionProperties.from_dict(_properties)

        config: Union[Unset, IssueFieldOptionConfiguration] = UNSET
        _config = d.pop("config", UNSET)
        if not isinstance(_config, Unset):
            config = IssueFieldOptionConfiguration.from_dict(_config)

        issue_field_option = cls(
            id_=id_,
            value=value,
            properties=properties,
            config=config,
        )

        return issue_field_option
