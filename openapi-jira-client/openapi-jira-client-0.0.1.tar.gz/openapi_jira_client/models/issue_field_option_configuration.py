from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.componentsschemas_issue_field_option_configuration_attributes_item import (
    ComponentsschemasIssueFieldOptionConfigurationAttributesItem,
)
from ..models.issue_field_option_scope_bean import IssueFieldOptionScopeBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueFieldOptionConfiguration")


@attr.s(auto_attribs=True)
class IssueFieldOptionConfiguration:
    """ Details of the projects the option is available in. """

    scope: Union[Unset, IssueFieldOptionScopeBean] = UNSET
    attributes: Union[Unset, List[ComponentsschemasIssueFieldOptionConfigurationAttributesItem]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        scope: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.to_dict()

        attributes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = []
            for attributes_item_data in self.attributes:
                attributes_item = attributes_item_data.value

                attributes.append(attributes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if scope is not UNSET:
            field_dict["scope"] = scope
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scope: Union[Unset, IssueFieldOptionScopeBean] = UNSET
        _scope = d.pop("scope", UNSET)
        if not isinstance(_scope, Unset):
            scope = IssueFieldOptionScopeBean.from_dict(_scope)

        attributes = []
        _attributes = d.pop("attributes", UNSET)
        for attributes_item_data in _attributes or []:
            attributes_item = ComponentsschemasIssueFieldOptionConfigurationAttributesItem(attributes_item_data)

            attributes.append(attributes_item)

        issue_field_option_configuration = cls(
            scope=scope,
            attributes=attributes,
        )

        return issue_field_option_configuration
