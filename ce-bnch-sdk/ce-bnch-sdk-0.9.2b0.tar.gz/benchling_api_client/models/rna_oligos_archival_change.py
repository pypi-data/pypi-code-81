from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RnaOligosArchivalChange")


@attr.s(auto_attribs=True)
class RnaOligosArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of Oligos along with any IDs of batches that were archived / unarchived."""

    batch_ids: Union[Unset, List[str]] = UNSET
    rna_oligo_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.batch_ids, Unset):
            batch_ids = self.batch_ids

        rna_oligo_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.rna_oligo_ids, Unset):
            rna_oligo_ids = self.rna_oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids
        if rna_oligo_ids is not UNSET:
            field_dict["rnaOligoIds"] = rna_oligo_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_ids = cast(List[str], d.pop("batchIds", UNSET))

        rna_oligo_ids = cast(List[str], d.pop("rnaOligoIds", UNSET))

        rna_oligos_archival_change = cls(
            batch_ids=batch_ids,
            rna_oligo_ids=rna_oligo_ids,
        )

        return rna_oligos_archival_change
