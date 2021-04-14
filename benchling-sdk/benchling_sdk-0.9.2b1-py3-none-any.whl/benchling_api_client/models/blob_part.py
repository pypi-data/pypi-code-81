from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlobPart")


@attr.s(auto_attribs=True)
class BlobPart:
    """  """

    e_tag: Union[Unset, str] = UNSET
    part_number: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        e_tag = self.e_tag
        part_number = self.part_number

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if e_tag is not UNSET:
            field_dict["eTag"] = e_tag
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        e_tag = d.pop("eTag", UNSET)

        part_number = d.pop("partNumber", UNSET)

        blob_part = cls(
            e_tag=e_tag,
            part_number=part_number,
        )

        return blob_part
