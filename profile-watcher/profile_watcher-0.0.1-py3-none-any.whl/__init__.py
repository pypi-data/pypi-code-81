#!/usr/bin/python
# A python library that provides update when
# something changes in social profiles.
# Copyright (C) 2021 Shubhendra Kushwaha
# @TheShubhendra shubhendrakushwaha94@gmail.com
# This file is a part of profile-watcher <https://github.com/TheShubhendra/profile-watcher>.
#
# profile-watcher is a free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# profile-watcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with profile-watcher.  If not, see <http://www.gnu.org/licenses/>.
from .watcher import watcher


__all__ = [watcher]
