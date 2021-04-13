from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.rna_oligo import RnaOligo

T = TypeVar("T", bound="RnaOligosPaginatedList")


@attr.s(auto_attribs=True)
class RnaOligosPaginatedList:
    """  """

    rna_oligos: List[RnaOligo]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        rna_oligos = []
        for rna_oligos_item_data in self.rna_oligos:
            rna_oligos_item = rna_oligos_item_data.to_dict()

            rna_oligos.append(rna_oligos_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "rnaOligos": rna_oligos,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rna_oligos = []
        _rna_oligos = d.pop("rnaOligos")
        for rna_oligos_item_data in _rna_oligos:
            rna_oligos_item = RnaOligo.from_dict(rna_oligos_item_data)

            rna_oligos.append(rna_oligos_item)

        next_token = d.pop("nextToken")

        rna_oligos_paginated_list = cls(
            rna_oligos=rna_oligos,
            next_token=next_token,
        )

        return rna_oligos_paginated_list
