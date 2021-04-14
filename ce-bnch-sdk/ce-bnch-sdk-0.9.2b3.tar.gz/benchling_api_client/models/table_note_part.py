from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entry_link import EntryLink
from ..models.entry_table import EntryTable
from ..models.table_note_part_type import TableNotePartType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TableNotePart")


@attr.s(auto_attribs=True)
class TableNotePart:
    """  """

    table: Union[Unset, EntryTable] = UNSET
    type: Union[Unset, TableNotePartType] = UNSET
    indentation: Union[Unset, int] = 0
    links: Union[Unset, List[EntryLink]] = UNSET
    text: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        table: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.table, Unset):
            table = self.table.to_dict()

        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        indentation = self.indentation
        links: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()

                links.append(links_item)

        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if table is not UNSET:
            field_dict["table"] = table
        if type is not UNSET:
            field_dict["type"] = type
        if indentation is not UNSET:
            field_dict["indentation"] = indentation
        if links is not UNSET:
            field_dict["links"] = links
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        table: Union[Unset, EntryTable] = UNSET
        _table = d.pop("table", UNSET)
        if not isinstance(_table, Unset):
            table = EntryTable.from_dict(_table)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = TableNotePartType(_type)

        indentation = d.pop("indentation", UNSET)

        links = []
        _links = d.pop("links", UNSET)
        for links_item_data in _links or []:
            links_item = EntryLink.from_dict(links_item_data)

            links.append(links_item)

        text = d.pop("text", UNSET)

        table_note_part = cls(
            table=table,
            type=type,
            indentation=indentation,
            links=links,
            text=text,
        )

        return table_note_part
