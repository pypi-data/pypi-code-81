from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.dna_oligos_archive_reason import DnaOligosArchiveReason

T = TypeVar("T", bound="DnaOligosArchive")


@attr.s(auto_attribs=True)
class DnaOligosArchive:
    """The request body for archiving DNA Oligos."""

    dna_oligo_ids: List[str]
    reason: DnaOligosArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        dna_oligo_ids = self.dna_oligo_ids

        reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaOligoIds": dna_oligo_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_oligo_ids = cast(List[str], d.pop("dnaOligoIds"))

        reason = DnaOligosArchiveReason(d.pop("reason"))

        dna_oligos_archive = cls(
            dna_oligo_ids=dna_oligo_ids,
            reason=reason,
        )

        return dna_oligos_archive
