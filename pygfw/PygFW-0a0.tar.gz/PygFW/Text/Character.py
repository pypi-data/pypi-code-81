from PygFW.Data import DataContainer
from PygFW.Data.Manipulator import JoinLists

alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphanumeric = """ 1234567890-=!\"£$%^&*()_+[]#{}~;':@,./<>?|\\"""

class Character:

    def __call__(self, character):

        self.__init__(character)

    def __init__(self, character):

        self._character = character if character in JoinLists(alphabet, alphabet.upper(), alphanumeric) and len(character) == 1 else 'a'

    @property
    def character(self):

        return self._character

    @character.setter
    def character(self, character):

        self.__init__(character)

    @property
    def upper(self):

        return self._character.upper()

    @property
    def lower(self):

        return self._character.lower()

class CharacterCollection:

    def __init__(self, characters=[]):

        self.characters = DataContainer()

        for character in characters:

            self.characters.add(character)

    @property
    def string(self):

        return ''.join(character.character for character in self.characters._list_)

    def construct(self):

        pass

    def strip(self, strip_string, strip_end=False):

        pass

