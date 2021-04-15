from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.auto_complete_suggestion import AutoCompleteSuggestion
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoCompleteSuggestions")


@attr.s(auto_attribs=True)
class AutoCompleteSuggestions:
    """ The results from a JQL query. """

    results: Union[Unset, List[AutoCompleteSuggestion]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()

                results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = AutoCompleteSuggestion.from_dict(results_item_data)

            results.append(results_item)

        auto_complete_suggestions = cls(
            results=results,
        )

        return auto_complete_suggestions
