from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.audit_record_bean import AuditRecordBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditRecords")


@attr.s(auto_attribs=True)
class AuditRecords:
    """ Container for a list of audit records. """

    offset: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    records: Union[Unset, List[AuditRecordBean]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        offset = self.offset
        limit = self.limit
        total = self.total
        records: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.records, Unset):
            records = []
            for records_item_data in self.records:
                records_item = records_item_data.to_dict()

                records.append(records_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if offset is not UNSET:
            field_dict["offset"] = offset
        if limit is not UNSET:
            field_dict["limit"] = limit
        if total is not UNSET:
            field_dict["total"] = total
        if records is not UNSET:
            field_dict["records"] = records

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        offset = d.pop("offset", UNSET)

        limit = d.pop("limit", UNSET)

        total = d.pop("total", UNSET)

        records = []
        _records = d.pop("records", UNSET)
        for records_item_data in _records or []:
            records_item = AuditRecordBean.from_dict(records_item_data)

            records.append(records_item)

        audit_records = cls(
            offset=offset,
            limit=limit,
            total=total,
            records=records,
        )

        return audit_records
