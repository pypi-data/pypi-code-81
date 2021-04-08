from pydecidim.model.abstract_api_element import AbstractApiElement
from pydecidim.model.translated_field import TranslatedField


class ComponentInterface(AbstractApiElement):
    """
    Represents a Component Interface from the Decidim API.

    Even thought in GraphQL a ComponentInterface is considered an interface, it contains fields, for this reason,
    ComponentInterface is defined as a class.
    """

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> TranslatedField:
        return self.__name

    @property
    def weight(self) -> int:
        return self.__weight

    def __init__(self, component_id: str, name: TranslatedField, weight: int) -> None:
        self.__id: str = component_id
        self.__name: TranslatedField = name
        self.__weight: int = weight
