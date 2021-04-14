from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.blob_create_type import BlobCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BlobCreate")


@attr.s(auto_attribs=True)
class BlobCreate:
    """  """

    data64: str
    md5: str
    name: str
    type: BlobCreateType
    mime_type: Union[Unset, str] = "application/octet-stream"

    def to_dict(self) -> Dict[str, Any]:
        data64 = self.data64
        md5 = self.md5
        name = self.name
        type = self.type.value

        mime_type = self.mime_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "data64": data64,
                "md5": md5,
                "name": name,
                "type": type,
            }
        )
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data64 = d.pop("data64")

        md5 = d.pop("md5")

        name = d.pop("name")

        type = BlobCreateType(d.pop("type"))

        mime_type = d.pop("mimeType", UNSET)

        blob_create = cls(
            data64=data64,
            md5=md5,
            name=name,
            type=type,
            mime_type=mime_type,
        )

        return blob_create
