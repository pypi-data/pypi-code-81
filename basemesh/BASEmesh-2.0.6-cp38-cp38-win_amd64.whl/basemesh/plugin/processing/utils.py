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

"""Utilities related to the processing submodule."""

from typing import Optional


def parse_docstring(string: Optional[str]) -> str:
    """Convert a Python docstring for use as an algorithm help text.

    This ignores any leading and trailing whitespace and only keeps
    double linebreaks.

    Parameters
    ----------
    string : Optional[str]
        A docstring to parse into a QGIS help text

    Returns
    -------
    str
        The formatted docstring, or an empty string if no docstring was
        passed
    """
    out_string = ''
    if string is not None:
        for line in string.splitlines():
            line = line.strip()

            # Keep empty lines
            if line == '':
                out_string += '\n\n'
            # Any other lines get appended as normal
            else:
                out_string += f' {line}'
    return out_string
