from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DnaOligosUnarchive")


@attr.s(auto_attribs=True)
class DnaOligosUnarchive:
    """The request body for unarchiving DNA Oligos."""

    dna_oligo_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        dna_oligo_ids = self.dna_oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaOligoIds": dna_oligo_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_oligo_ids = cast(List[str], d.pop("dnaOligoIds"))

        dna_oligos_unarchive = cls(
            dna_oligo_ids=dna_oligo_ids,
        )

        return dna_oligos_unarchive
