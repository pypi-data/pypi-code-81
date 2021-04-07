"""Mountable IndieWeb apps and helper functions."""

from ... import mm
from .. import framework as fw
from . import indieauth
from . import micropub
from . import microsub
from . import webmention
from . import websub

__all__ = ["indieauth", "micropub", "microsub", "webmention", "websub",
           "cache_app"]


cache_app = fw.application("Cache", db=False, mount_prefix="cache",
                           resource=r".+")
tmpl = mm.templates(__name__)


@cache_app.route(r"")
class CacheIndex:

    def _get(self):
        return tmpl.cache(fw.tx.db.select("cache"))


@cache_app.route(r"{resource}")
class CacheResource:

    def _get(self):
        return tmpl.cache(fw.tx.db.select("cache", where="url = ?",
                          vals=[self.resource]))
