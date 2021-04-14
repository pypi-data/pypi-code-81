from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..models.entry_table_row import EntryTableRow
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryTable")


@attr.s(auto_attribs=True)
class EntryTable:
    """Actual tabular data with rows and columns of text on the note."""

    column_labels: Union[Unset, List[Optional[str]]] = UNSET
    name: Union[Unset, str] = UNSET
    rows: Union[Unset, List[EntryTableRow]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        column_labels: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.column_labels, Unset):
            column_labels = self.column_labels

        name = self.name
        rows: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.rows, Unset):
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data.to_dict()

                rows.append(rows_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if column_labels is not UNSET:
            field_dict["columnLabels"] = column_labels
        if name is not UNSET:
            field_dict["name"] = name
        if rows is not UNSET:
            field_dict["rows"] = rows

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column_labels = cast(List[Optional[str]], d.pop("columnLabels", UNSET))

        name = d.pop("name", UNSET)

        rows = []
        _rows = d.pop("rows", UNSET)
        for rows_item_data in _rows or []:
            rows_item = EntryTableRow.from_dict(rows_item_data)

            rows.append(rows_item)

        entry_table = cls(
            column_labels=column_labels,
            name=name,
            rows=rows,
        )

        return entry_table
