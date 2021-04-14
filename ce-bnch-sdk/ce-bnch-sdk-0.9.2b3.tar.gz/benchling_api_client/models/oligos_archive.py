from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.oligos_archive_reason import OligosArchiveReason

T = TypeVar("T", bound="OligosArchive")


@attr.s(auto_attribs=True)
class OligosArchive:
    """The request body for archiving Oligos."""

    oligo_ids: List[str]
    reason: OligosArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        oligo_ids = self.oligo_ids

        reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "oligoIds": oligo_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oligo_ids = cast(List[str], d.pop("oligoIds"))

        reason = OligosArchiveReason(d.pop("reason"))

        oligos_archive = cls(
            oligo_ids=oligo_ids,
            reason=reason,
        )

        return oligos_archive
