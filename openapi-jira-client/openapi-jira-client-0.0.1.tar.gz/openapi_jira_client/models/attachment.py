import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.user_details import UserDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="Attachment")


@attr.s(auto_attribs=True)
class Attachment:
    """ Details about an attachment. """

    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    author: Union[Unset, UserDetails] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    size: Union[Unset, int] = UNSET
    mime_type: Union[Unset, str] = UNSET
    content: Union[Unset, str] = UNSET
    thumbnail: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id_ = self.id_
        filename = self.filename
        author: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        size = self.size
        mime_type = self.mime_type
        content = self.content
        thumbnail = self.thumbnail

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if filename is not UNSET:
            field_dict["filename"] = filename
        if author is not UNSET:
            field_dict["author"] = author
        if created is not UNSET:
            field_dict["created"] = created
        if size is not UNSET:
            field_dict["size"] = size
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type
        if content is not UNSET:
            field_dict["content"] = content
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        filename = d.pop("filename", UNSET)

        author: Union[Unset, UserDetails] = UNSET
        _author = d.pop("author", UNSET)
        if not isinstance(_author, Unset):
            author = UserDetails.from_dict(_author)

        created: Union[Unset, datetime.datetime] = UNSET
        _created = d.pop("created", UNSET)
        if not isinstance(_created, Unset):
            created = isoparse(_created)

        size = d.pop("size", UNSET)

        mime_type = d.pop("mimeType", UNSET)

        content = d.pop("content", UNSET)

        thumbnail = d.pop("thumbnail", UNSET)

        attachment = cls(
            self_=self_,
            id_=id_,
            filename=filename,
            author=author,
            created=created,
            size=size,
            mime_type=mime_type,
            content=content,
            thumbnail=thumbnail,
        )

        attachment.additional_properties = d
        return attachment

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
