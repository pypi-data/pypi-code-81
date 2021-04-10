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

from pathlib import Path
from tempfile import TemporaryDirectory

from f4ratk.directories import Cache


def given_path_when_register_should_create_all_directories_in_path():
    with TemporaryDirectory(prefix='f4ratk_test_tmp_') as parent:
        target_path = Path(parent, 'intermediate', 'target')

        Cache.register(str(target_path))

        assert target_path.exists()
        assert target_path.is_dir()


def given_cache_when_file_with_name_requested_should_append_name_to_cache_path():
    with TemporaryDirectory(prefix='f4ratk_test_tmp_') as parent:
        result = Cache.register(parent).file('target')
        assert result == Path(parent, 'target')
