"""
shop.py
-----------

Create or update a remote Shop with new machines or pricing,
referenced by shopId. Note that the authorization for this
comes from the userId of the API key.

The most recent generated REST API documentation is available at:
https://api.kerfed.com/docs/v1
"""

import requests


class _Shop(object):
    """
    The base class for a Shop object.
    """

    def __init__(self, shopId):
        """

        Parameters
        ----------
        shopId : str
          The identifier for the shop.
        """
        # create a session containing the API key
        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self._API_KEY})
        # save the reference for the shop ID
        self.shopId = shopId

    def create(self):
        response = self._session.post(
            '{root}/shops/{shopId}'.format(
                root=self._API_ROOT, shopId=self.shopId))
        if not response.ok:
            raise ValueError(response.text)
        return response.json()

    @property
    def info(self):
        """
        Get the shop's basic information that is presented
        to unpriviliged frontend clients.

        Returns
        ---------

        info : dict
          Basic information about a shop
        """
        response = self._session.get(
            '{root}/shops/{shopId}'.format(
                root=self._API_ROOT, shopId=self.shopId))
        if not response.ok:
            raise ValueError(response.text)
        return response.json()

    @property
    def edit(self):
        """
        Get a full copy of the shop doc, including pricing.

        Returns
        ---------
        info_raw : dict
          Fill shop document
        """
        response = self._session.get(
            '{root}/shop/{shopId}/edit'.format(
                root=self._API_ROOT, shopId=self.shopId))
        if not response.ok:
            raise ValueError(response.text)
        return response.json()

    @edit.setter
    def edit(self, values):
        """
        """
        response = self._session.put(
            '{root}/shop/{shopId}/edit'.format(
                root=self._API_ROOT, shopId=self.shopId),
            json={"shopContent": values})
        if not response.ok:
            raise ValueError(response.text)
        return response.json()
