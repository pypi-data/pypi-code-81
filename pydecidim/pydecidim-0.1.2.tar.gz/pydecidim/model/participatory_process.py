from typing import List

from pydecidim.model.abstract_api_element import AbstractApiElement
from pydecidim.model.component_interface import ComponentInterface
from pydecidim.model.translated_field import TranslatedField


class ParticipatoryProcess(AbstractApiElement):
    """
    Represents a Participatory Process from the Decidim API.
    """

    @property
    def id(self) -> str:
        return self.__id

    @property
    def title(self) -> TranslatedField:
        return self.__title

    @property
    def created_at(self) -> str:
        return self.__created_at

    @property
    def components(self) -> List[ComponentInterface] or None:
        return self.__components

    def __init__(self,
                 process_id: str,
                 title: TranslatedField,
                 created_at: str,
                 components: List[ComponentInterface] or None) -> None:
        self.__id: str = process_id
        self.__created_at: str = created_at
        self.__title: TranslatedField = title
        self.__components: List[ComponentInterface] = components
