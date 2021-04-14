from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.translation_regions_item import TranslationRegionsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="Translation")


@attr.s(auto_attribs=True)
class Translation:
    """  """

    amino_acids: Union[Unset, str] = UNSET
    end: Union[Unset, int] = UNSET
    regions: Union[Unset, List[TranslationRegionsItem]] = UNSET
    start: Union[Unset, int] = UNSET
    strand: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        amino_acids = self.amino_acids
        end = self.end
        regions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.regions, Unset):
            regions = []
            for regions_item_data in self.regions:
                regions_item = regions_item_data.to_dict()

                regions.append(regions_item)

        start = self.start
        strand = self.strand

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if amino_acids is not UNSET:
            field_dict["aminoAcids"] = amino_acids
        if end is not UNSET:
            field_dict["end"] = end
        if regions is not UNSET:
            field_dict["regions"] = regions
        if start is not UNSET:
            field_dict["start"] = start
        if strand is not UNSET:
            field_dict["strand"] = strand

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amino_acids = d.pop("aminoAcids", UNSET)

        end = d.pop("end", UNSET)

        regions = []
        _regions = d.pop("regions", UNSET)
        for regions_item_data in _regions or []:
            regions_item = TranslationRegionsItem.from_dict(regions_item_data)

            regions.append(regions_item)

        start = d.pop("start", UNSET)

        strand = d.pop("strand", UNSET)

        translation = cls(
            amino_acids=amino_acids,
            end=end,
            regions=regions,
            start=start,
            strand=strand,
        )

        return translation
