from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.assay_result import AssayResult
from ..models.request_response_samples_item import RequestResponseSamplesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestResponse")


@attr.s(auto_attribs=True)
class RequestResponse:
    """  """

    results: Union[Unset, List[AssayResult]] = UNSET
    samples: Union[Unset, List[RequestResponseSamplesItem]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        results: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()

                results.append(results_item)

        samples: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.samples, Unset):
            samples = []
            for samples_item_data in self.samples:
                samples_item = samples_item_data.to_dict()

                samples.append(samples_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if results is not UNSET:
            field_dict["results"] = results
        if samples is not UNSET:
            field_dict["samples"] = samples

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = AssayResult.from_dict(results_item_data)

            results.append(results_item)

        samples = []
        _samples = d.pop("samples", UNSET)
        for samples_item_data in _samples or []:
            samples_item = RequestResponseSamplesItem.from_dict(samples_item_data)

            samples.append(samples_item)

        request_response = cls(
            results=results,
            samples=samples,
        )

        return request_response
