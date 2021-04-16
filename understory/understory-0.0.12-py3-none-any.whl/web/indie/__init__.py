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
people_app = fw.application("People", db=False, mount_prefix="people",
                            person=r".+")
tmpl = mm.templates(__name__)


@cache_app.route(r"")
class Cache:

    def _get(self):
        return tmpl.cache(fw.tx.db.select("cache"))


@cache_app.route(r"{resource}")
class Resource:

    def _get(self):
        try:
            resource = fw.tx.db.select("cache", where="url = ?",
                                       vals=[f"https://{self.resource}"])[0]
        except IndexError:
            resource = fw.tx.db.select("cache", where="url = ?",
                                       vals=[f"http://{self.resource}"])[0]
        return tmpl.cache_resource(resource)


@people_app.route(r"")
class People:

    def _get(self):
        return tmpl.people(fw.tx.db.select("subscriptions"))


@people_app.route(r"{person}")
class Person:

    def _get(self):
        try:
            resource = fw.tx.db.select("cache", where="url = ?",
                                       vals=[f"https://{self.resource}"])[0]
        except IndexError:
            resource = fw.tx.db.select("cache", where="url = ?",
                                       vals=[f"http://{self.resource}"])[0]
        return tmpl.cache_resource(resource)
