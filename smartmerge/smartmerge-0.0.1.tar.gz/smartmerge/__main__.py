# Copyright (C) 2020 Breezy Developers
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import argparse
import sys

from . import smartmerge, load_plugins

parser = argparse.ArgumentParser()

parser.add_argument('--git', action='store_true')
parser.add_argument('base', type=str)
parser.add_argument('this', type=str)
parser.add_argument('other', type=str)
parser.add_argument('conflictlen', nargs='?', type=int)

args = parser.parse_args()

load_plugins()

with open(args.this, 'rt') as f:
    this = f.readlines()
with open(args.base, 'rt') as f:
    base = f.readlines()
with open(args.other, 'rt') as f:
    other = f.readlines()

merged_lines = smartmerge(base, this, other)

sys.stdout.writelines(merged_lines)
