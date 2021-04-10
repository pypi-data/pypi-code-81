##############################################################################
# Copyright (C) 2020 - 2021 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of F4RATK.
#
# F4RATK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from os import getenv
from pathlib import Path
from typing import Union

from flask_caching import Cache

from f4ratk.directories import cache


def locate_cache_dir() -> Union[str, Path]:
    return getenv('CACHE_DIR', cache.file('server'))


def create_cache() -> Cache:
    cache_type = getenv('CACHE_TYPE')
    cache_dir = locate_cache_dir() if cache_type == 'FileSystemCache' else None

    config = dict()

    if cache_type:
        config['CACHE_TYPE'] = cache_type

    if cache_dir:
        config['CACHE_DIR'] = cache_dir

    return Cache(config=config)


server_cache = create_cache()
