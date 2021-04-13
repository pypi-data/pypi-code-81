from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.folder import Folder

T = TypeVar("T", bound="FoldersPaginatedList")


@attr.s(auto_attribs=True)
class FoldersPaginatedList:
    """  """

    folders: List[Folder]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        folders = []
        for folders_item_data in self.folders:
            folders_item = folders_item_data.to_dict()

            folders.append(folders_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "folders": folders,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folders = []
        _folders = d.pop("folders")
        for folders_item_data in _folders:
            folders_item = Folder.from_dict(folders_item_data)

            folders.append(folders_item)

        next_token = d.pop("nextToken")

        folders_paginated_list = cls(
            folders=folders,
            next_token=next_token,
        )

        return folders_paginated_list
