from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaTemplateAlignmentFile")


@attr.s(auto_attribs=True)
class DnaTemplateAlignmentFile:
    """  """

    data: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        data = self.data
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = d.pop("data", UNSET)

        name = d.pop("name", UNSET)

        dna_template_alignment_file = cls(
            data=data,
            name=name,
        )

        return dna_template_alignment_file
