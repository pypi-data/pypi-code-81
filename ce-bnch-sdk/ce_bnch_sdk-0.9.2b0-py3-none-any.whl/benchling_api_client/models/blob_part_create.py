from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="BlobPartCreate")


@attr.s(auto_attribs=True)
class BlobPartCreate:
    """  """

    data64: str
    md5: str
    part_number: int

    def to_dict(self) -> Dict[str, Any]:
        data64 = self.data64
        md5 = self.md5
        part_number = self.part_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "data64": data64,
                "md5": md5,
                "partNumber": part_number,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data64 = d.pop("data64")

        md5 = d.pop("md5")

        part_number = d.pop("partNumber")

        blob_part_create = cls(
            data64=data64,
            md5=md5,
            part_number=part_number,
        )

        return blob_part_create
