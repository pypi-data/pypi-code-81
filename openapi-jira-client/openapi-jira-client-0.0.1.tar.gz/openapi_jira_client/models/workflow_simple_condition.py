from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.componentsschemas_workflow_simple_condition_configuration import (
    ComponentsschemasWorkflowSimpleConditionConfiguration,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowSimpleCondition")


@attr.s(auto_attribs=True)
class WorkflowSimpleCondition:
    """ A workflow transition condition rule. """

    type_: str
    node_type: str
    configuration: Union[Unset, ComponentsschemasWorkflowSimpleConditionConfiguration] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type_ = self.type_
        node_type = self.node_type
        configuration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = self.configuration.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "nodeType": node_type,
            }
        )
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = d.pop("type")

        node_type = d.pop("nodeType")

        configuration: Union[Unset, ComponentsschemasWorkflowSimpleConditionConfiguration] = UNSET
        _configuration = d.pop("configuration", UNSET)
        if not isinstance(_configuration, Unset):
            configuration = ComponentsschemasWorkflowSimpleConditionConfiguration.from_dict(_configuration)

        workflow_simple_condition = cls(
            type_=type_,
            node_type=node_type,
            configuration=configuration,
        )

        workflow_simple_condition.additional_properties = d
        return workflow_simple_condition

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
