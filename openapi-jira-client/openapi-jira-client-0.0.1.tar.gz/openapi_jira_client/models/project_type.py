from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectType")


@attr.s(auto_attribs=True)
class ProjectType:
    """ Details about a project type. """

    key: Union[Unset, str] = UNSET
    formatted_key: Union[Unset, str] = UNSET
    description_i18n_key: Union[Unset, str] = UNSET
    icon: Union[Unset, str] = UNSET
    color: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        formatted_key = self.formatted_key
        description_i18n_key = self.description_i18n_key
        icon = self.icon
        color = self.color

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if formatted_key is not UNSET:
            field_dict["formattedKey"] = formatted_key
        if description_i18n_key is not UNSET:
            field_dict["descriptionI18nKey"] = description_i18n_key
        if icon is not UNSET:
            field_dict["icon"] = icon
        if color is not UNSET:
            field_dict["color"] = color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        formatted_key = d.pop("formattedKey", UNSET)

        description_i18n_key = d.pop("descriptionI18nKey", UNSET)

        icon = d.pop("icon", UNSET)

        color = d.pop("color", UNSET)

        project_type = cls(
            key=key,
            formatted_key=formatted_key,
            description_i18n_key=description_i18n_key,
            icon=icon,
            color=color,
        )

        return project_type
