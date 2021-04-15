"""
order.py
-----------

Create a new remote Order from an existing Quote,
or load an existing one referenced by orderId.

The most recent generated REST API documentation is available at:
https://api.kerfed.com/docs/v1
"""

# requests is the only non-stdlib dependency
import requests


class _Order(object):
    """
    The base class for a remote Order object, or a
    Quote with options such as quantity "baked" into
    an immutable structure.
    """

    def __init__(self, orderId):
        # create a session containing the API key
        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self._API_KEY})
        # save the orderId
        self.orderId = orderId

    @property
    def info(self):
        """
        Add a CAD file to the quote which will be processed
        automatically.

        Parameters
        -----------
        file_obj : None or str
          File to upload to the Kerfed Engine.
        file_type : None or str
          Type of file if not a filename.
        """
        response = self._session.get(
            '{root}/orders/{orderId}'.format(
                root=self._API_ROOT, orderId=self.orderId))
        if not response.ok:
            raise ValueError(response.text)
        return response.json()

    def shared_link(self, expiration=None):
        """
        Get a shared link to the current Orders.

        Parameters
        ----------
        expiration : None or int
          Expiration duration in seconds

        Returns
        --------
        link : str
          URL to a shared link containing Orders.
        """
        if expiration is None:
            # if not set use one day
            expiration = 24 * 60 * 60

        response = self._session.post(
            '{root}/orders/{orderId}/share'.format(
                root=self._API_ROOT, orderId=self.orderId),
            json={"expiration": expiration})

        if not response.ok:
            raise ValueError(response.text)
        # TODO : check out lazy iteration
        blob = response.json()
        return blob['link']

    @property
    def files(self):
        """
        Get a list of files attached to this quote.

        Returns
        ---------
        files : list
          List of dict with file information.
        """
        response = self._session.get(
            '{root}/orders/{orderId}/files'.format(
                root=self._API_ROOT, orderId=self.orderId))
        if not response.ok:
            raise ValueError(response.text)
        # TODO : check out lazy iteration
        blob = response.json()
        return blob['items']

    @property
    def parts(self):
        """
        Get manufacturing analysis and prices for unique parts
        attached to this quote.

        Returns
        ----------
        parts : dict
          Keyed by partId
        """
        response = self._session.get(
            '{root}/orders/{orderId}/parts'.format(
                root=self._API_ROOT, orderId=self.orderId))
        if not response.ok:
            raise ValueError(response.text)
        blob = response.json()
        return blob['items']

    def __del__(self, *args, **kwargs):
        self._session.close()
