from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaSequencesArchivalChange")


@attr.s(auto_attribs=True)
class DnaSequencesArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of DNA sequences along with any IDs of batches that were archived / unarchived."""

    batch_ids: Union[Unset, List[str]] = UNSET
    dna_sequence_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.batch_ids, Unset):
            batch_ids = self.batch_ids

        dna_sequence_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.dna_sequence_ids, Unset):
            dna_sequence_ids = self.dna_sequence_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids
        if dna_sequence_ids is not UNSET:
            field_dict["dnaSequenceIds"] = dna_sequence_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_ids = cast(List[str], d.pop("batchIds", UNSET))

        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds", UNSET))

        dna_sequences_archival_change = cls(
            batch_ids=batch_ids,
            dna_sequence_ids=dna_sequence_ids,
        )

        return dna_sequences_archival_change
