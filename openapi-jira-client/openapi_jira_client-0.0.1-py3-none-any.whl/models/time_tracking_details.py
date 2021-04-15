from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeTrackingDetails")


@attr.s(auto_attribs=True)
class TimeTrackingDetails:
    """ Time tracking details. """

    original_estimate: Union[Unset, str] = UNSET
    remaining_estimate: Union[Unset, str] = UNSET
    time_spent: Union[Unset, str] = UNSET
    original_estimate_seconds: Union[Unset, int] = UNSET
    remaining_estimate_seconds: Union[Unset, int] = UNSET
    time_spent_seconds: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        original_estimate = self.original_estimate
        remaining_estimate = self.remaining_estimate
        time_spent = self.time_spent
        original_estimate_seconds = self.original_estimate_seconds
        remaining_estimate_seconds = self.remaining_estimate_seconds
        time_spent_seconds = self.time_spent_seconds

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if original_estimate is not UNSET:
            field_dict["originalEstimate"] = original_estimate
        if remaining_estimate is not UNSET:
            field_dict["remainingEstimate"] = remaining_estimate
        if time_spent is not UNSET:
            field_dict["timeSpent"] = time_spent
        if original_estimate_seconds is not UNSET:
            field_dict["originalEstimateSeconds"] = original_estimate_seconds
        if remaining_estimate_seconds is not UNSET:
            field_dict["remainingEstimateSeconds"] = remaining_estimate_seconds
        if time_spent_seconds is not UNSET:
            field_dict["timeSpentSeconds"] = time_spent_seconds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        original_estimate = d.pop("originalEstimate", UNSET)

        remaining_estimate = d.pop("remainingEstimate", UNSET)

        time_spent = d.pop("timeSpent", UNSET)

        original_estimate_seconds = d.pop("originalEstimateSeconds", UNSET)

        remaining_estimate_seconds = d.pop("remainingEstimateSeconds", UNSET)

        time_spent_seconds = d.pop("timeSpentSeconds", UNSET)

        time_tracking_details = cls(
            original_estimate=original_estimate,
            remaining_estimate=remaining_estimate,
            time_spent=time_spent,
            original_estimate_seconds=original_estimate_seconds,
            remaining_estimate_seconds=remaining_estimate_seconds,
            time_spent_seconds=time_spent_seconds,
        )

        return time_tracking_details
