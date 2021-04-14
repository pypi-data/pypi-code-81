from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..models.automation_output_processors_archive_reason import AutomationOutputProcessorsArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutomationOutputProcessorsArchive")


@attr.s(auto_attribs=True)
class AutomationOutputProcessorsArchive:
    """  """

    automation_output_processor_ids: List[str]
    reason: Union[Unset, AutomationOutputProcessorsArchiveReason] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        automation_output_processor_ids = self.automation_output_processor_ids

        reason: Union[Unset, int] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "automationOutputProcessorIds": automation_output_processor_ids,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        automation_output_processor_ids = cast(List[str], d.pop("automationOutputProcessorIds"))

        reason = None
        _reason = d.pop("reason", UNSET)
        if _reason is not None and _reason is not UNSET:
            reason = AutomationOutputProcessorsArchiveReason(_reason)

        automation_output_processors_archive = cls(
            automation_output_processor_ids=automation_output_processor_ids,
            reason=reason,
        )

        return automation_output_processors_archive
