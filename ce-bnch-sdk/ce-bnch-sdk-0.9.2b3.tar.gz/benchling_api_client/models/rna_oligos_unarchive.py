from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="RnaOligosUnarchive")


@attr.s(auto_attribs=True)
class RnaOligosUnarchive:
    """The request body for unarchiving RNA Oligos."""

    rna_oligo_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        rna_oligo_ids = self.rna_oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "rnaOligoIds": rna_oligo_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rna_oligo_ids = cast(List[str], d.pop("rnaOligoIds"))

        rna_oligos_unarchive = cls(
            rna_oligo_ids=rna_oligo_ids,
        )

        return rna_oligos_unarchive
