from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.componentsschemas_issue_field_option_create_bean_properties import (
    ComponentsschemasIssueFieldOptionCreateBeanProperties,
)
from ..models.issue_field_option_configuration import IssueFieldOptionConfiguration
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueFieldOptionCreateBean")


@attr.s(auto_attribs=True)
class IssueFieldOptionCreateBean:
    """  """

    value: str
    properties: Union[Unset, ComponentsschemasIssueFieldOptionCreateBeanProperties] = UNSET
    config: Union[Unset, IssueFieldOptionConfiguration] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
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
        value = d.pop("value")

        properties: Union[Unset, ComponentsschemasIssueFieldOptionCreateBeanProperties] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = ComponentsschemasIssueFieldOptionCreateBeanProperties.from_dict(_properties)

        config: Union[Unset, IssueFieldOptionConfiguration] = UNSET
        _config = d.pop("config", UNSET)
        if not isinstance(_config, Unset):
            config = IssueFieldOptionConfiguration.from_dict(_config)

        issue_field_option_create_bean = cls(
            value=value,
            properties=properties,
            config=config,
        )

        issue_field_option_create_bean.additional_properties = d
        return issue_field_option_create_bean

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
