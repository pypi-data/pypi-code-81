from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_issue_type_create_bean_type import ComponentsschemasIssueTypeCreateBeanType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeCreateBean")


@attr.s(auto_attribs=True)
class IssueTypeCreateBean:
    """  """

    name: str
    description: Union[Unset, str] = UNSET
    type_: Union[Unset, ComponentsschemasIssueTypeCreateBeanType] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description", UNSET)

        type_: Union[Unset, ComponentsschemasIssueTypeCreateBeanType] = UNSET
        _type_ = d.pop("type", UNSET)
        if not isinstance(_type_, Unset):
            type_ = ComponentsschemasIssueTypeCreateBeanType(_type_)

        issue_type_create_bean = cls(
            name=name,
            description=description,
            type_=type_,
        )

        return issue_type_create_bean
