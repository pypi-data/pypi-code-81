"""
Xero Contacts API
"""

from .api_base import ApiBase


class Contacts(ApiBase):
    """
    Class for Contacts API
    """

    GET_CONTACTS = '/api.xro/2.0/contacts'
    POST_CONTACTS = '/api.xro/2.0/contacts'
    SEARCH_CONTACT = '/api.xro/2.0/Contacts?where=Name="{0}"'

    def get_all(self):
        """
        Get all contacts

        Returns:
            List of all contacts
        """

        return self._get_request(Contacts.GET_CONTACTS)

    def post(self, data):
        """
        create new contact

        Parameters:
        data (dict): Data to create contact

        Returns:
             Response from API
        """

        return self._post_request(data, Contacts.POST_CONTACTS)

    def search_contact_by_contact_name(self, contact_name: str):
        """
        Search contact by Contact Name
        :param contact_name: Xero Contact Name
        :return: Contact
        """

        response = self._get_request(Contacts.SEARCH_CONTACT.format(contact_name))

        return response['Contacts'][0] if response['Contacts'] else None
