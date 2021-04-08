# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os
import sys

from ._config import Config


class Main:
    config: Config = None

    @classmethod
    def _get_config_path(cls):
        author = 'flowdas'
        filename = f'{author}.json'

        # ./test-config.json
        yield filename

        # $VIRTUAL_ENV/test-config.json
        if sys.prefix != sys.base_prefix or os.path.isdir(os.path.join(sys.prefix, 'conda-meta')):  # pragma: no cover
            yield os.path.join(sys.prefix, filename)

        # $XDG_CONFIG_HOME/flowdas/test-config.json
        home = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        yield os.path.join(home, author, filename)

        # $XDG_CONFIG_DIRS/flowdas/test-config.json
        paths = os.environ.get('XDG_CONFIG_DIRS', '/etc/xdg')
        for path in paths.split(':'):
            yield os.path.join(path, author, filename)

    @classmethod
    def init(cls):
        path = os.environ.get('FLOWDAS_CONFIG')
        if path is None:
            for path in cls._get_config_path():
                if os.path.exists(path):
                    break
            else:
                path = None
        if path is None:
            data = {}
        else:
            with open(path) as f:
                data = json.load(f)
        cls.config = Config(data)

    @classmethod
    def main(cls, args=None):
        cls.init()
        from ._console import ConsoleEndPoint
        for endpoint in cls.config.endpoints:
            if isinstance(endpoint, ConsoleEndPoint):
                console = endpoint
                break
        else:
            console = ConsoleEndPoint()
            cls.config.endpoints.append(console)
        return console.main(args)
