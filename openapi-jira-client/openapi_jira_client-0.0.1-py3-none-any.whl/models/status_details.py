from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.status_category import StatusCategory
from ..types import UNSET, Unset

T = TypeVar("T", bound="StatusDetails")


@attr.s(auto_attribs=True)
class StatusDetails:
    """ A status. """

    self_: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    icon_url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    status_category: Union[Unset, StatusCategory] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        description = self.description
        icon_url = self.icon_url
        name = self.name
        id_ = self.id_
        status_category: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.status_category, Unset):
            status_category = self.status_category.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if description is not UNSET:
            field_dict["description"] = description
        if icon_url is not UNSET:
            field_dict["iconUrl"] = icon_url
        if name is not UNSET:
            field_dict["name"] = name
        if id_ is not UNSET:
            field_dict["id"] = id_
        if status_category is not UNSET:
            field_dict["statusCategory"] = status_category

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        description = d.pop("description", UNSET)

        icon_url = d.pop("iconUrl", UNSET)

        name = d.pop("name", UNSET)

        id_ = d.pop("id", UNSET)

        status_category: Union[Unset, StatusCategory] = UNSET
        _status_category = d.pop("statusCategory", UNSET)
        if not isinstance(_status_category, Unset):
            status_category = StatusCategory.from_dict(_status_category)

        status_details = cls(
            self_=self_,
            description=description,
            icon_url=icon_url,
            name=name,
            id_=id_,
            status_category=status_category,
        )

        status_details.additional_properties = d
        return status_details

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
