from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entry_link import EntryLink
from ..models.external_file_note_part_type import ExternalFileNotePartType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalFileNotePart")


@attr.s(auto_attribs=True)
class ExternalFileNotePart:
    """  """

    external_file_id: Union[Unset, str] = UNSET
    type: Union[Unset, ExternalFileNotePartType] = UNSET
    indentation: Union[Unset, int] = 0
    links: Union[Unset, List[EntryLink]] = UNSET
    text: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        external_file_id = self.external_file_id
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
        if external_file_id is not UNSET:
            field_dict["externalFileId"] = external_file_id
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
        external_file_id = d.pop("externalFileId", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = ExternalFileNotePartType(_type)

        indentation = d.pop("indentation", UNSET)

        links = []
        _links = d.pop("links", UNSET)
        for links_item_data in _links or []:
            links_item = EntryLink.from_dict(links_item_data)

            links.append(links_item)

        text = d.pop("text", UNSET)

        external_file_note_part = cls(
            external_file_id=external_file_id,
            type=type,
            indentation=indentation,
            links=links,
            text=text,
        )

        return external_file_note_part
