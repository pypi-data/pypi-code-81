from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.oligo_create import OligoCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaOligosBulkCreateRequest")


@attr.s(auto_attribs=True)
class DnaOligosBulkCreateRequest:
    """  """

    dna_oligos: Union[Unset, List[OligoCreate]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        dna_oligos: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.dna_oligos, Unset):
            dna_oligos = []
            for dna_oligos_item_data in self.dna_oligos:
                dna_oligos_item = dna_oligos_item_data.to_dict()

                dna_oligos.append(dna_oligos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if dna_oligos is not UNSET:
            field_dict["dnaOligos"] = dna_oligos

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_oligos = []
        _dna_oligos = d.pop("dnaOligos", UNSET)
        for dna_oligos_item_data in _dna_oligos or []:
            dna_oligos_item = OligoCreate.from_dict(dna_oligos_item_data)

            dna_oligos.append(dna_oligos_item)

        dna_oligos_bulk_create_request = cls(
            dna_oligos=dna_oligos,
        )

        return dna_oligos_bulk_create_request
