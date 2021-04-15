from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="HistoryMetadataParticipant")


@attr.s(auto_attribs=True)
class HistoryMetadataParticipant:
    """ Details of user or system associated with a issue history metadata item. """

    id_: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    display_name_key: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    avatar_url: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        display_name = self.display_name
        display_name_key = self.display_name_key
        type_ = self.type_
        avatar_url = self.avatar_url
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if display_name_key is not UNSET:
            field_dict["displayNameKey"] = display_name_key
        if type_ is not UNSET:
            field_dict["type"] = type_
        if avatar_url is not UNSET:
            field_dict["avatarUrl"] = avatar_url
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        display_name = d.pop("displayName", UNSET)

        display_name_key = d.pop("displayNameKey", UNSET)

        type_ = d.pop("type", UNSET)

        avatar_url = d.pop("avatarUrl", UNSET)

        url = d.pop("url", UNSET)

        history_metadata_participant = cls(
            id_=id_,
            display_name=display_name,
            display_name_key=display_name_key,
            type_=type_,
            avatar_url=avatar_url,
            url=url,
        )

        history_metadata_participant.additional_properties = d
        return history_metadata_participant

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
