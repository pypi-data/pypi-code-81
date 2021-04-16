import attr
import girder_client

from nlidatamanagement.utils.girder_instance import GirderInstance


@attr.s(kw_only=True)
class GirderConnector(object):
    """A python girder client for Girder server connection."""
    _client = attr.ib(init=False, default=None)
    _user_info = attr.ib(init=False, default=None)
    _girder_instance = attr.ib(init=False, default=None)

    def connect(self, girder_instance: GirderInstance):
        self._client = girder_client.GirderClient(apiUrl=girder_instance.host)
        user_id = self._client.authenticate(apiKey=girder_instance.api_key)['_id']
        self._user_info = self._client.getUser(user_id)
        self._girder_instance = girder_instance

    def is_connected(self, girder_instance: GirderInstance):
        return self._girder_instance and self._girder_instance == girder_instance

    @property
    def first_name(self):
        return self._user_info['firstName']

    @property
    def last_name(self):
        return self._user_info['lastName']

    @property
    def client(self):
        return self._client

    @property
    def instance(self):
        return self._girder_instance
