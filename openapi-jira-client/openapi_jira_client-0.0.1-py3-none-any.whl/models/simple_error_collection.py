from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_simple_error_collection_errors import ComponentsschemasSimpleErrorCollectionErrors
from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleErrorCollection")


@attr.s(auto_attribs=True)
class SimpleErrorCollection:
    """  """

    errors: Union[Unset, ComponentsschemasSimpleErrorCollectionErrors] = UNSET
    error_messages: Union[Unset, List[str]] = UNSET
    http_status_code: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        errors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors.to_dict()

        error_messages: Union[Unset, List[str]] = UNSET
        if not isinstance(self.error_messages, Unset):
            error_messages = self.error_messages

        http_status_code = self.http_status_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if errors is not UNSET:
            field_dict["errors"] = errors
        if error_messages is not UNSET:
            field_dict["errorMessages"] = error_messages
        if http_status_code is not UNSET:
            field_dict["httpStatusCode"] = http_status_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        errors: Union[Unset, ComponentsschemasSimpleErrorCollectionErrors] = UNSET
        _errors = d.pop("errors", UNSET)
        if not isinstance(_errors, Unset):
            errors = ComponentsschemasSimpleErrorCollectionErrors.from_dict(_errors)

        error_messages = cast(List[str], d.pop("errorMessages", UNSET))

        http_status_code = d.pop("httpStatusCode", UNSET)

        simple_error_collection = cls(
            errors=errors,
            error_messages=error_messages,
            http_status_code=http_status_code,
        )

        return simple_error_collection
