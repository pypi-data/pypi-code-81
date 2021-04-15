from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.comment import Comment
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaginatedResponseComment")


@attr.s(auto_attribs=True)
class PaginatedResponseComment:
    """  """

    total: Union[Unset, int] = UNSET
    max_results: Union[Unset, int] = UNSET
    start_at: Union[Unset, int] = UNSET
    results: Union[Unset, List[Comment]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        total = self.total
        max_results = self.max_results
        start_at = self.start_at
        results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()

                results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if total is not UNSET:
            field_dict["total"] = total
        if max_results is not UNSET:
            field_dict["maxResults"] = max_results
        if start_at is not UNSET:
            field_dict["startAt"] = start_at
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total = d.pop("total", UNSET)

        max_results = d.pop("maxResults", UNSET)

        start_at = d.pop("startAt", UNSET)

        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = Comment.from_dict(results_item_data)

            results.append(results_item)

        paginated_response_comment = cls(
            total=total,
            max_results=max_results,
            start_at=start_at,
            results=results,
        )

        return paginated_response_comment
