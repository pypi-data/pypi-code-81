from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.rna_oligos_archive_reason import RnaOligosArchiveReason

T = TypeVar("T", bound="RnaOligosArchive")


@attr.s(auto_attribs=True)
class RnaOligosArchive:
    """The request body for archiving RNA Oligos."""

    reason: RnaOligosArchiveReason
    rna_oligo_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        rna_oligo_ids = self.rna_oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "rnaOligoIds": rna_oligo_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = RnaOligosArchiveReason(d.pop("reason"))

        rna_oligo_ids = cast(List[str], d.pop("rnaOligoIds"))

        rna_oligos_archive = cls(
            reason=reason,
            rna_oligo_ids=rna_oligo_ids,
        )

        return rna_oligos_archive
