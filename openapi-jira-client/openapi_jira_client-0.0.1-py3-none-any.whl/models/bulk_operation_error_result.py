from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.error_collection import ErrorCollection
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkOperationErrorResult")


@attr.s(auto_attribs=True)
class BulkOperationErrorResult:
    """  """

    status: Union[Unset, int] = UNSET
    element_errors: Union[Unset, ErrorCollection] = UNSET
    failed_element_number: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        element_errors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.element_errors, Unset):
            element_errors = self.element_errors.to_dict()

        failed_element_number = self.failed_element_number

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if element_errors is not UNSET:
            field_dict["elementErrors"] = element_errors
        if failed_element_number is not UNSET:
            field_dict["failedElementNumber"] = failed_element_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status", UNSET)

        element_errors: Union[Unset, ErrorCollection] = UNSET
        _element_errors = d.pop("elementErrors", UNSET)
        if not isinstance(_element_errors, Unset):
            element_errors = ErrorCollection.from_dict(_element_errors)

        failed_element_number = d.pop("failedElementNumber", UNSET)

        bulk_operation_error_result = cls(
            status=status,
            element_errors=element_errors,
            failed_element_number=failed_element_number,
        )

        return bulk_operation_error_result
