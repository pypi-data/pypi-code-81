# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import asyncio
import getopt
import inspect
import json
import pprint
import sys
import traceback

from typeable import cast, JsonValue

from ._config import Config, EndPoint
from ._injector import Injector
from ._main import Main

_COMMAND = '__COMMAND'


class _Command:
    __slots__ = (
        'function',
    )

    def __init__(self, *, function):
        self.function = function


def command(_=None, *, name=None):
    def deco(func):
        setattr(func, _COMMAND, _Command(
            function=cast.function(func, keep_async=False),
        ))
        return func

    return deco if _ is None else deco(_)


class DefaultConsoleRoot:
    @command
    def config(self):
        return Main.config

    @command
    def run(self):
        from typeable import cast, JsonValue
        import uvicorn
        from ._http import HttpEndPoint

        app = None
        for endpoint in Main.config.endpoints:
            if isinstance(endpoint, HttpEndPoint):
                app = endpoint.get_app()
                break
        if app:
            opts = cast(JsonValue, Main.config.uvicorn)
            uvicorn.run(app, **opts)

    @command
    def version(self):
        if sys.version_info >= (3, 8):  # pragma: no cover
            # noinspection PyCompatibility
            from importlib.metadata import version
            ver = version('flowdas')
        else:  # pragma: no cover
            from pkg_resources import get_distribution
            ver = getattr(get_distribution('flowdas'), 'version')
        print(ver)


class ConsoleEndPoint(EndPoint, kind='console'):
    _root = None

    root_class: type = DefaultConsoleRoot

    @property
    def root(self):
        if self._root is None:
            self._root = self.root_class()
        return self._root

    def _parse_args(self, _args):
        args = []
        kwargs = {}
        for arg in _args:
            idx = arg.find('=')
            if idx >= 0:
                key = arg[:idx]
                if key.isidentifier():
                    val = arg[idx + 1:]
                    try:
                        val = json.loads(val)
                    except:
                        pass
                    kwargs[key] = val
                    continue
            if kwargs:
                raise SyntaxError("positional argument follows keyword argument")
            try:
                val = json.loads(arg)
            except:
                val = arg
            args.append(val)
        return args, kwargs

    def dispatch(self, injector, node, args, opts):
        if not args:
            return self.help_group(node)
        name = args[0]
        attr = getattr(node, name, None)
        if attr is None:
            return self._error(name)
        if inspect.ismethod(attr):
            cmd = getattr(attr, _COMMAND, None)
            if cmd is None:
                return self._error(name)
            args, kwargs = self._parse_args(args[1:])
            if 'h' in opts:
                return self.help_command(attr, cmd, args, kwargs)
            else:
                return injector.dispatch(cmd.function, node, *args, **kwargs)
        if name.startswith('_'):
            return self._error(name)
        return self.dispatch(injector, attr, args[1:], opts)

    def _print_command_help(self, method):
        functor = ConsoleInjector.instrument(method)
        print(f"{method.__name__}{functor.signature}")

    def help_command(self, method, cmd, args, kwargs):
        self._print_command_help(method)
        sys.exit(2)

    def help_group(self, node):
        print('Commands:\n')
        methods = inspect.getmembers(node, inspect.ismethod)
        for name, method in sorted(methods):
            cmd = getattr(method, _COMMAND, None)
            if cmd is not None:
                self._print_command_help(method)
        sys.exit(2)

    def _error(self, name):
        print(f"'{name}' is not a command.")
        sys.exit(2)

    def main(self, args=None):
        if args is None:  # pragma: no cover
            args = sys.argv[1:]
        try:
            optlist, args = getopt.getopt(args, 'dh')
        except getopt.GetoptError:
            return self.help_group(self.root)
        opts = ''.join(sorted(opt[1:] for opt, _ in optlist))
        if 'd' in opts:
            Main.config.debug = True
        injector = ConsoleInjector()
        injector.insert(ConsoleEndPoint, self)
        try:
            result = self.dispatch(injector, self.root, args, opts)
            if inspect.isawaitable(result):
                result = asyncio.get_event_loop().run_until_complete(result)
            if result is not None:
                pprint.pprint(cast(JsonValue, result))
        except Exception as e:
            if Main.config.debug:
                traceback.print_exc()
            else:
                print(f"{e.__class__.__name__}: {e}")
            return 1
        return 0


class ConsoleInjector(Injector):
    pass


ConsoleInjector.register(ConsoleEndPoint)(None)
