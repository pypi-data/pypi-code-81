#!/usr/bin/env python

# A component of the BASEmesh pre-processing toolkit.
# Copyright (C) 2020  ETH Zürich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Module-level script dispatcher for BASEmesh.

This script acts as a shortcut to access other scripts and shared
utilities available in BASEmesh.

Enter `--help` for a list of all available modules, along with a brief
description.

"""

import argparse
import subprocess
import sys

from basemesh import __version__ as version


if __name__ == '__main__':
    print('\n'
          '---------------------------------------\n'
          f'BASEmesh - Version {version}\n'
          '---------------------------------------\n')

    # Set up argument parser
    parser = argparse.ArgumentParser(
        'BASEmesh', description='Module-level script dispatcher', epilog='\n')
    # Define submodules
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--1D', dest='target', action='store_const', const='basechange',
        help='BASEchange 1D channel generator')

    # Consume remaining arguments
    #
    # NOTE: This will not catch any exact duplicates at the very beginning of
    # the command, e.g. "python -m basemesh --1D --1D" would both be "eaten" by
    # by this script.
    # However, "python -m basemesh --1D -something else --1D" will be forwarded
    # as expected.
    parser.add_argument('command', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    # Run the associated script
    subprocess.call(
        (sys.executable, '-m', f'basemesh.{args.target}', *args.command))
