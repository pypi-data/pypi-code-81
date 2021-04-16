#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020, 2021 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Prompt String-like Print
'''

import os
from pathlib import Path
import sys

from .printer import PrintSpace


# Initiate default print function
def init_print(custom: str = None) -> PrintSpace:
    '''
    Initiate ps-print function with default marks
    and marks read from various psprintrc configurarion files:

    Args:
        custom: custom configuration file location

    '''
    # psprintrc file locations
    user_home = Path(os.environ["HOME"]).resolve()
    config = os.environ.get("XDG_CONFIG_HOME", user_home.joinpath(".config"))
    rc_locations = {
        'root': Path("/etc/psprint/style.yml"),
        'user': user_home.joinpath(".psprintrc"),  # bad
        'config': Path(config).joinpath("psprint", "style.yml"),  # good
        'local': Path(".psprintrc").resolve(),
        'custom': Path(custom) if custom else None,
    }

    default_config = Path(__file__).parent.joinpath("style.yml")
    default_print = PrintSpace(config=default_config)

    for loc in ('root', 'user', 'config', 'local', 'custom'):
        # DONT: loc from tuple, not keys(), deliberately to ascertain order
        if rc_locations[loc] is not None:
            if rc_locations[loc].is_file():  # type: ignore
                default_print.set_opts(rc_locations[loc])

    if 'idlelib.run' in sys.modules or not sys.stdout.isatty():
        # Running inside idle
        default_print.switches['bland'] = True
    return default_print


DEFAULT_PRINT = init_print()
'''
PrintSpace object created by reading defaults from various
psprintrc and psprint/style.yml files

'''


print = DEFAULT_PRINT.psprint
'''
psprint function for imports

'''


__all__ = ['DEFAULT_PRINT', 'print']


__version__ = "1!1.0.3"
