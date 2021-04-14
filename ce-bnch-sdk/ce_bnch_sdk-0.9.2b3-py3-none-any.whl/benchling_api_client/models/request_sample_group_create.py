from typing import Any, Dict, Type, TypeVar

import attr

from ..models.request_sample_group_samples import RequestSampleGroupSamples

T = TypeVar("T", bound="RequestSampleGroupCreate")


@attr.s(auto_attribs=True)
class RequestSampleGroupCreate:
    """  """

    samples: RequestSampleGroupSamples

    def to_dict(self) -> Dict[str, Any]:
        samples = self.samples.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "samples": samples,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        samples = RequestSampleGroupSamples.from_dict(d.pop("samples"))

        request_sample_group_create = cls(
            samples=samples,
        )

        return request_sample_group_create
