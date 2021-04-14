from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="NotePart")


@attr.s(auto_attribs=True)
class NotePart:
    """Notes are the main building blocks of entries. Each note corresponds roughly to a paragraph and has one of these types: - 'text': plain text - 'code': preformatted code block - 'table': a table with rows and columns of text - 'list_bullet': one "line" of a bulleted list - 'list_number': one "line" of a numbered list - 'list_checkbox': one "line" of a checklist - 'external_file': an attached user-uploaded file"""

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        src_dict.copy()
        note_part = cls()

        return note_part
