from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.dna_oligo import DnaOligo

T = TypeVar("T", bound="DnaOligosPaginatedList")


@attr.s(auto_attribs=True)
class DnaOligosPaginatedList:
    """  """

    dna_oligos: List[DnaOligo]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        dna_oligos = []
        for dna_oligos_item_data in self.dna_oligos:
            dna_oligos_item = dna_oligos_item_data.to_dict()

            dna_oligos.append(dna_oligos_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaOligos": dna_oligos,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_oligos = []
        _dna_oligos = d.pop("dnaOligos")
        for dna_oligos_item_data in _dna_oligos:
            dna_oligos_item = DnaOligo.from_dict(dna_oligos_item_data)

            dna_oligos.append(dna_oligos_item)

        next_token = d.pop("nextToken")

        dna_oligos_paginated_list = cls(
            dna_oligos=dna_oligos,
            next_token=next_token,
        )

        return dna_oligos_paginated_list
