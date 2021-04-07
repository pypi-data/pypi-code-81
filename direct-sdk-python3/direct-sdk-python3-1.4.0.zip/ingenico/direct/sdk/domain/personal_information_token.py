# -*- coding: utf-8 -*-
#
# This class was auto-generated from the API references found at
# https://support.direct.ingenico.com/documentation/api/reference/
#
from ingenico.direct.sdk.data_object import DataObject
from ingenico.direct.sdk.domain.personal_name_token import PersonalNameToken


class PersonalInformationToken(DataObject):

    __name = None

    @property
    def name(self) -> PersonalNameToken:
        """
        Type: :class:`ingenico.direct.sdk.domain.personal_name_token.PersonalNameToken`
        """
        return self.__name

    @name.setter
    def name(self, value: PersonalNameToken):
        self.__name = value

    def to_dictionary(self):
        dictionary = super(PersonalInformationToken, self).to_dictionary()
        if self.name is not None:
            dictionary['name'] = self.name.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary):
        super(PersonalInformationToken, self).from_dictionary(dictionary)
        if 'name' in dictionary:
            if not isinstance(dictionary['name'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['name']))
            value = PersonalNameToken()
            self.name = value.from_dictionary(dictionary['name'])
        return self
