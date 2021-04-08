from polzyFunctions.utils import get_file_path, Singleton
from logging import getLogger
from polzyFunctions.GlobalConstants import GlobalConstants
from polzyFunctions.translator.DataHandler import Data

logger = getLogger(GlobalConstants.loggerName)


class Translator(metaclass=Singleton):
    """
    We are making this class singleton to share same default language on multiple instances.
    """
    def __init__(self, default="en"):
        logger.debug("Language translation backend module initialized - buffered")
        self.default_language = default.lower()
        self.data = Data().data  # getting data from singleton class's attribute

    def translate(self, word, language=None):
        if not language:
            language = self.default_language
        language = language.lower()
        if language == "en":
            return word
        try:
            result = self.data.get(word).get(language)
        except:
            result = word
            logger.info(f'Translation of "{word}" for language "{language}" not found!')
        return result

    def add_translation_dict(self, dict):
        # this method is to be used when we need to update translation from dictionary. It can be called in sub repo
        # for customer specific translations.
        # structure of input dictionary: {"English word": {"de": "translation for it", "wi": "translation for it", ...}}
        self.data.update(dict)

    def add_translation_file(self, fileNameAndPath):
        # this method is to be used when we need to update translation from json file. It can be called in sub repo
        # for customer specific translations.
        # structure in input json file: {"English word": {"de": "translation for it", "wi": "translation for it", ...}}
        fileNameAndPath = get_file_path(fileNameAndPath)
        self.add_translation_dict(Data.get_data(fileNameAndPath))

    def update_default_language(self, language):
        # this method is planned to be used to update default language of translation module as per current user
        self.default_language = language.lower()
