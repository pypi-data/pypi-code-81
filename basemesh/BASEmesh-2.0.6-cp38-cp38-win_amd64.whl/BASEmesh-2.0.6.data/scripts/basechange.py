#!python

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

"""Command line script for the BASEchange channel generator.

This script exposes the core functionality of the BASEchange submodule
and allows the creation of 1D channel geometries from the given input
parameters.

Run this script with the "--help" for additional information and
detailed argument descriptions.
"""

import os
import subprocess
import sys

try:
    # pylint: disable=import-error, unused-import
    import basemesh.basechange
except ModuleNotFoundError as err:
    basemesh_dir, _ = os.path.split(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(basemesh_dir)
    try:
        import basemesh.basechange
    except ModuleNotFoundError:
        raise err from err
else:
    basemesh_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    # Update PYTHONPATH
    path = os.environ.get('PYTHONPATH', '')
    if path:
        path += ':'
    path += os.path.abspath(basemesh_dir)
    os.environ['PYTHONPATH'] = path
    # Get script path
    subprocess.call(
        (sys.executable, '-m', 'basemesh', '--1D', *sys.argv[1:]))
