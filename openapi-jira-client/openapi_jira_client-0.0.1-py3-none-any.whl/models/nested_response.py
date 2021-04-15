from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.error_collection import ErrorCollection
from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedResponse")


@attr.s(auto_attribs=True)
class NestedResponse:
    """  """

    status: Union[Unset, int] = UNSET
    error_collection: Union[Unset, ErrorCollection] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        error_collection: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_collection, Unset):
            error_collection = self.error_collection.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if error_collection is not UNSET:
            field_dict["errorCollection"] = error_collection

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status", UNSET)

        error_collection: Union[Unset, ErrorCollection] = UNSET
        _error_collection = d.pop("errorCollection", UNSET)
        if not isinstance(_error_collection, Unset):
            error_collection = ErrorCollection.from_dict(_error_collection)

        nested_response = cls(
            status=status,
            error_collection=error_collection,
        )

        return nested_response
