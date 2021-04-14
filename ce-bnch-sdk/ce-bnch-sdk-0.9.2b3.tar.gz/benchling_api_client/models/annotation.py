from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Annotation")


@attr.s(auto_attribs=True)
class Annotation:
    """  """

    color: Union[Unset, str] = UNSET
    end: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    start: Union[Unset, int] = UNSET
    strand: Union[Unset, int] = UNSET
    type: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        color = self.color
        end = self.end
        name = self.name
        start = self.start
        strand = self.strand
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if end is not UNSET:
            field_dict["end"] = end
        if name is not UNSET:
            field_dict["name"] = name
        if start is not UNSET:
            field_dict["start"] = start
        if strand is not UNSET:
            field_dict["strand"] = strand
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color", UNSET)

        end = d.pop("end", UNSET)

        name = d.pop("name", UNSET)

        start = d.pop("start", UNSET)

        strand = d.pop("strand", UNSET)

        type = d.pop("type", UNSET)

        annotation = cls(
            color=color,
            end=end,
            name=name,
            start=start,
            strand=strand,
            type=type,
        )

        return annotation
