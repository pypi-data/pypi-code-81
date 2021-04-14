from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaOligosArchivalChange")


@attr.s(auto_attribs=True)
class DnaOligosArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of Oligos along with any IDs of batches that were archived / unarchived."""

    batch_ids: Union[Unset, List[str]] = UNSET
    dna_oligo_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.batch_ids, Unset):
            batch_ids = self.batch_ids

        dna_oligo_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.dna_oligo_ids, Unset):
            dna_oligo_ids = self.dna_oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids
        if dna_oligo_ids is not UNSET:
            field_dict["dnaOligoIds"] = dna_oligo_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_ids = cast(List[str], d.pop("batchIds", UNSET))

        dna_oligo_ids = cast(List[str], d.pop("dnaOligoIds", UNSET))

        dna_oligos_archival_change = cls(
            batch_ids=batch_ids,
            dna_oligo_ids=dna_oligo_ids,
        )

        return dna_oligos_archival_change
