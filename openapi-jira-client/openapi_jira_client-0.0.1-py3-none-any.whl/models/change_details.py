from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangeDetails")


@attr.s(auto_attribs=True)
class ChangeDetails:
    """ A change item. """

    field: Union[Unset, str] = UNSET
    fieldtype: Union[Unset, str] = UNSET
    field_id: Union[Unset, str] = UNSET
    from_: Union[Unset, str] = UNSET
    from_string: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    to_string: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        field = self.field
        fieldtype = self.fieldtype
        field_id = self.field_id
        from_ = self.from_
        from_string = self.from_string
        to = self.to
        to_string = self.to_string

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if field is not UNSET:
            field_dict["field"] = field
        if fieldtype is not UNSET:
            field_dict["fieldtype"] = fieldtype
        if field_id is not UNSET:
            field_dict["fieldId"] = field_id
        if from_ is not UNSET:
            field_dict["from"] = from_
        if from_string is not UNSET:
            field_dict["fromString"] = from_string
        if to is not UNSET:
            field_dict["to"] = to
        if to_string is not UNSET:
            field_dict["toString"] = to_string

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field = d.pop("field", UNSET)

        fieldtype = d.pop("fieldtype", UNSET)

        field_id = d.pop("fieldId", UNSET)

        from_ = d.pop("from", UNSET)

        from_string = d.pop("fromString", UNSET)

        to = d.pop("to", UNSET)

        to_string = d.pop("toString", UNSET)

        change_details = cls(
            field=field,
            fieldtype=fieldtype,
            field_id=field_id,
            from_=from_,
            from_string=from_string,
            to=to,
            to_string=to_string,
        )

        return change_details
