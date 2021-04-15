from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_error_collection_errors import ComponentsschemasErrorCollectionErrors
from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorCollection")


@attr.s(auto_attribs=True)
class ErrorCollection:
    """ Error messages from an operation. """

    error_messages: Union[Unset, List[str]] = UNSET
    errors: Union[Unset, ComponentsschemasErrorCollectionErrors] = UNSET
    status: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        error_messages: Union[Unset, List[str]] = UNSET
        if not isinstance(self.error_messages, Unset):
            error_messages = self.error_messages

        errors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors.to_dict()

        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if error_messages is not UNSET:
            field_dict["errorMessages"] = error_messages
        if errors is not UNSET:
            field_dict["errors"] = errors
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        error_messages = cast(List[str], d.pop("errorMessages", UNSET))

        errors: Union[Unset, ComponentsschemasErrorCollectionErrors] = UNSET
        _errors = d.pop("errors", UNSET)
        if not isinstance(_errors, Unset):
            errors = ComponentsschemasErrorCollectionErrors.from_dict(_errors)

        status = d.pop("status", UNSET)

        error_collection = cls(
            error_messages=error_messages,
            errors=errors,
            status=status,
        )

        return error_collection
