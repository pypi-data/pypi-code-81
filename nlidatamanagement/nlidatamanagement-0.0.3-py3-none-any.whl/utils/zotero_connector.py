import attr
from pyzotero import zotero

from nlidatamanagement.utils.zotero_instance import ZoteroInstance


@attr.s(kw_only=True)
class ZoteroConnector(object):
    """A python zotero client for Girder server connection."""
    _client = attr.ib(init=False, default=None)
    _zotero_instance = attr.ib(init=False, default=None)

    def connect(self, zotero_instance: ZoteroInstance):
        self._client = zotero.Zotero(zotero_instance.library_id, zotero_instance.library_type, zotero_instance.api_key)
        self._zotero_instance = zotero_instance

    def is_connected(self, zotero_instance: ZoteroInstance):
        return self._zotero_instance and self._zotero_instance == zotero_instance

    @property
    def client(self):
        return self._client

    @property
    def instance(self):
        return self._zotero_instance
