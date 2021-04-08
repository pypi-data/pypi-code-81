from __future__ import annotations

from typing import List, Dict, Tuple

from pydecidim.model.abstract_api_element import AbstractApiElement


class TranslatedField(AbstractApiElement):
    """
    Represents a TranslatedField from the Decidim API.
    """

    @staticmethod
    def parse_from_gql(gql_list: List[dict]) -> TranslatedField:
        translations: Dict[str, str] = dict()
        for translation_dict in gql_list:
            locale = translation_dict['locale']
            text = translation_dict['text']
            translations[locale] = text
        return TranslatedField(translations)

    @property
    def locales(self) -> Tuple[str]:
        return tuple(self.__translations.keys())

    def get_translations(self, locales: List[str]) -> Dict[str, str]:
        """
        Gets dictionary of translation given a list of language codes. Example: ["en", "ca"]

        :param locales: A list of language codes.
        :return: A dictionary with the format language_code -> translation.
        """
        return {key: self.__translations[key] if key in self.__translations else None for key in locales}

    def get_translation(self, locale: str) -> str or None:
        """
        Gets a translation for a specific language code, or None if the language code doesn't have any translation.
        :param locale: The language code to retrieve.
        :return: A str with the required translation. None if the translation doesn't exists.
        """
        if locale in self.__translations:
            return self.__translations[locale]
        else:
            return None

    def __init__(self, translations: Dict[str, str]) -> None:
        self.__translations: Dict[str, str] = translations
