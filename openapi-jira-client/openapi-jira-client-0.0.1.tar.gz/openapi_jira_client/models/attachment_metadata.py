import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.componentsschemas_attachment_metadata_properties import ComponentsschemasAttachmentMetadataProperties
from ..models.user import User
from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentMetadata")


@attr.s(auto_attribs=True)
class AttachmentMetadata:
    """ Metadata for an issue attachment. """

    id_: Union[Unset, int] = UNSET
    self_: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    author: Union[Unset, User] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    size: Union[Unset, int] = UNSET
    mime_type: Union[Unset, str] = UNSET
    properties: Union[Unset, ComponentsschemasAttachmentMetadataProperties] = UNSET
    content: Union[Unset, str] = UNSET
    thumbnail: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        self_ = self.self_
        filename = self.filename
        author: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        size = self.size
        mime_type = self.mime_type
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        content = self.content
        thumbnail = self.thumbnail

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if self_ is not UNSET:
            field_dict["self"] = self_
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
        if properties is not UNSET:
            field_dict["properties"] = properties
        if content is not UNSET:
            field_dict["content"] = content
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        filename = d.pop("filename", UNSET)

        author: Union[Unset, User] = UNSET
        _author = d.pop("author", UNSET)
        if not isinstance(_author, Unset):
            author = User.from_dict(_author)

        created: Union[Unset, datetime.datetime] = UNSET
        _created = d.pop("created", UNSET)
        if not isinstance(_created, Unset):
            created = isoparse(_created)

        size = d.pop("size", UNSET)

        mime_type = d.pop("mimeType", UNSET)

        properties: Union[Unset, ComponentsschemasAttachmentMetadataProperties] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = ComponentsschemasAttachmentMetadataProperties.from_dict(_properties)

        content = d.pop("content", UNSET)

        thumbnail = d.pop("thumbnail", UNSET)

        attachment_metadata = cls(
            id_=id_,
            self_=self_,
            filename=filename,
            author=author,
            created=created,
            size=size,
            mime_type=mime_type,
            properties=properties,
            content=content,
            thumbnail=thumbnail,
        )

        return attachment_metadata
