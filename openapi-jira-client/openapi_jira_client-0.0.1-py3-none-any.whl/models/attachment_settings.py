from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentSettings")


@attr.s(auto_attribs=True)
class AttachmentSettings:
    """ Details of the instance's attachment settings. """

    enabled: Union[Unset, bool] = UNSET
    upload_limit: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        upload_limit = self.upload_limit

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if upload_limit is not UNSET:
            field_dict["uploadLimit"] = upload_limit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        upload_limit = d.pop("uploadLimit", UNSET)

        attachment_settings = cls(
            enabled=enabled,
            upload_limit=upload_limit,
        )

        return attachment_settings
