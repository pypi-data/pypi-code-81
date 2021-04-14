from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.batches_archive_reason import BatchesArchiveReason

T = TypeVar("T", bound="BatchesArchive")


@attr.s(auto_attribs=True)
class BatchesArchive:
    """The request body for archiving Batches."""

    batch_ids: List[str]
    reason: BatchesArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        batch_ids = self.batch_ids

        reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "batchIds": batch_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_ids = cast(List[str], d.pop("batchIds"))

        reason = BatchesArchiveReason(d.pop("reason"))

        batches_archive = cls(
            batch_ids=batch_ids,
            reason=reason,
        )

        return batches_archive
