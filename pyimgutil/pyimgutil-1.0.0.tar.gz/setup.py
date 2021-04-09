"""This is a shim for use with pyproject.toml and setup.cfg.

A pyproject.toml file and a setup.cfg file render setup.py unnecessary
for the most part. However, this shim is still required in order to
have an editable install.

Copyright (C) 2021 emerac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import setuptools

if __name__ == "__main__":
    setuptools.setup()
