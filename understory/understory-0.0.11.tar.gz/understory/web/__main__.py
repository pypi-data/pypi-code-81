"""Command line tools for the web."""

from pprint import pprint

from understory import term
from understory import web

__all__ = ["main"]


main = term.application("web", web.__doc__)


@main.register()
class Serve:

    def setup(self, add_arg):
        add_arg("app", help="name of web application")

    def run(self, stdin, log):
        __import__(self.app + ".__web__")
        web.serve(self.app)
        return 0


@main.register()
class MF:

    def setup(self, add_arg):
        add_arg("uri", help="address of the resource to GET and parse for MF")

    def run(self, stdin, log):
        pprint(web.get(self.uri).mf2json)
        return 0


@main.register()
class Subscribe:

    def setup(self, add_arg):
        add_arg("uri", help="address of the resource to GET")

    def run(self, stdin, log):
        for patch_range, patch_body in web.subscribe(self.uri):
            print(patch_range)
            print(patch_body)
            print()
        return 0
