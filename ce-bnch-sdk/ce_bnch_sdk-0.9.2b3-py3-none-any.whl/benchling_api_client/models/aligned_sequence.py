from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AlignedSequence")


@attr.s(auto_attribs=True)
class AlignedSequence:
    """  """

    bases: Union[Unset, str] = UNSET
    dna_sequence_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    trim_end: Union[Unset, int] = UNSET
    trim_start: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        bases = self.bases
        dna_sequence_id = self.dna_sequence_id
        name = self.name
        trim_end = self.trim_end
        trim_start = self.trim_start

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if bases is not UNSET:
            field_dict["bases"] = bases
        if dna_sequence_id is not UNSET:
            field_dict["dnaSequenceId"] = dna_sequence_id
        if name is not UNSET:
            field_dict["name"] = name
        if trim_end is not UNSET:
            field_dict["trimEnd"] = trim_end
        if trim_start is not UNSET:
            field_dict["trimStart"] = trim_start

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bases = d.pop("bases", UNSET)

        dna_sequence_id = d.pop("dnaSequenceId", UNSET)

        name = d.pop("name", UNSET)

        trim_end = d.pop("trimEnd", UNSET)

        trim_start = d.pop("trimStart", UNSET)

        aligned_sequence = cls(
            bases=bases,
            dna_sequence_id=dna_sequence_id,
            name=name,
            trim_end=trim_end,
            trim_start=trim_start,
        )

        return aligned_sequence
