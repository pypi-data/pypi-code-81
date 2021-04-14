from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Primer")


@attr.s(auto_attribs=True)
class Primer:
    """  """

    bases: Union[Unset, str] = UNSET
    bind_position: Union[Unset, int] = UNSET
    color: Union[Unset, str] = UNSET
    end: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    oligo_id: Union[Unset, str] = UNSET
    overhang_length: Union[Unset, int] = UNSET
    start: Union[Unset, int] = UNSET
    strand: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        bases = self.bases
        bind_position = self.bind_position
        color = self.color
        end = self.end
        name = self.name
        oligo_id = self.oligo_id
        overhang_length = self.overhang_length
        start = self.start
        strand = self.strand

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if bases is not UNSET:
            field_dict["bases"] = bases
        if bind_position is not UNSET:
            field_dict["bindPosition"] = bind_position
        if color is not UNSET:
            field_dict["color"] = color
        if end is not UNSET:
            field_dict["end"] = end
        if name is not UNSET:
            field_dict["name"] = name
        if oligo_id is not UNSET:
            field_dict["oligoId"] = oligo_id
        if overhang_length is not UNSET:
            field_dict["overhangLength"] = overhang_length
        if start is not UNSET:
            field_dict["start"] = start
        if strand is not UNSET:
            field_dict["strand"] = strand

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bases = d.pop("bases", UNSET)

        bind_position = d.pop("bindPosition", UNSET)

        color = d.pop("color", UNSET)

        end = d.pop("end", UNSET)

        name = d.pop("name", UNSET)

        oligo_id = d.pop("oligoId", UNSET)

        overhang_length = d.pop("overhangLength", UNSET)

        start = d.pop("start", UNSET)

        strand = d.pop("strand", UNSET)

        primer = cls(
            bases=bases,
            bind_position=bind_position,
            color=color,
            end=end,
            name=name,
            oligo_id=oligo_id,
            overhang_length=overhang_length,
            start=start,
            strand=strand,
        )

        return primer
