from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentArchiveItemReadable")


@attr.s(auto_attribs=True)
class AttachmentArchiveItemReadable:
    """ Metadata for an item in an attachment archive. """

    path: Union[Unset, str] = UNSET
    index: Union[Unset, int] = UNSET
    size: Union[Unset, str] = UNSET
    media_type: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        index = self.index
        size = self.size
        media_type = self.media_type
        label = self.label

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if index is not UNSET:
            field_dict["index"] = index
        if size is not UNSET:
            field_dict["size"] = size
        if media_type is not UNSET:
            field_dict["mediaType"] = media_type
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path", UNSET)

        index = d.pop("index", UNSET)

        size = d.pop("size", UNSET)

        media_type = d.pop("mediaType", UNSET)

        label = d.pop("label", UNSET)

        attachment_archive_item_readable = cls(
            path=path,
            index=index,
            size=size,
            media_type=media_type,
            label=label,
        )

        return attachment_archive_item_readable
