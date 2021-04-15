from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_avatar_urls import ComponentsschemasAvatarUrls
from ..types import UNSET, Unset

T = TypeVar("T", bound="Avatar")


@attr.s(auto_attribs=True)
class Avatar:
    """ Details of an avatar. """

    id_: str
    owner: Union[Unset, str] = UNSET
    is_system_avatar: Union[Unset, bool] = UNSET
    is_selected: Union[Unset, bool] = UNSET
    is_deletable: Union[Unset, bool] = UNSET
    file_name: Union[Unset, str] = UNSET
    urls: Union[Unset, ComponentsschemasAvatarUrls] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        owner = self.owner
        is_system_avatar = self.is_system_avatar
        is_selected = self.is_selected
        is_deletable = self.is_deletable
        file_name = self.file_name
        urls: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.urls, Unset):
            urls = self.urls.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
            }
        )
        if owner is not UNSET:
            field_dict["owner"] = owner
        if is_system_avatar is not UNSET:
            field_dict["isSystemAvatar"] = is_system_avatar
        if is_selected is not UNSET:
            field_dict["isSelected"] = is_selected
        if is_deletable is not UNSET:
            field_dict["isDeletable"] = is_deletable
        if file_name is not UNSET:
            field_dict["fileName"] = file_name
        if urls is not UNSET:
            field_dict["urls"] = urls

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        owner = d.pop("owner", UNSET)

        is_system_avatar = d.pop("isSystemAvatar", UNSET)

        is_selected = d.pop("isSelected", UNSET)

        is_deletable = d.pop("isDeletable", UNSET)

        file_name = d.pop("fileName", UNSET)

        urls: Union[Unset, ComponentsschemasAvatarUrls] = UNSET
        _urls = d.pop("urls", UNSET)
        if not isinstance(_urls, Unset):
            urls = ComponentsschemasAvatarUrls.from_dict(_urls)

        avatar = cls(
            id_=id_,
            owner=owner,
            is_system_avatar=is_system_avatar,
            is_selected=is_selected,
            is_deletable=is_deletable,
            file_name=file_name,
            urls=urls,
        )

        return avatar
