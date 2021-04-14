from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.dna_sequence import DnaSequence

T = TypeVar("T", bound="DnaSequencesPaginatedList")


@attr.s(auto_attribs=True)
class DnaSequencesPaginatedList:
    """  """

    dna_sequences: List[DnaSequence]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        dna_sequences = []
        for dna_sequences_item_data in self.dna_sequences:
            dna_sequences_item = dna_sequences_item_data.to_dict()

            dna_sequences.append(dna_sequences_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaSequences": dna_sequences,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_sequences = []
        _dna_sequences = d.pop("dnaSequences")
        for dna_sequences_item_data in _dna_sequences:
            dna_sequences_item = DnaSequence.from_dict(dna_sequences_item_data)

            dna_sequences.append(dna_sequences_item)

        next_token = d.pop("nextToken")

        dna_sequences_paginated_list = cls(
            dna_sequences=dna_sequences,
            next_token=next_token,
        )

        return dna_sequences_paginated_list
