"""Matrix Manipulation module to add, substract, multiply matrices.

Copyright (C) 2021 Fares Ahmed

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

# Check this awesome GitHub repo
# https://github.com/navdeep-G/setup.py

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# Stolen from https://bitbucket.org/jeunice/stuf/src/master/setup.py :)
def getversion(fname):
    """Get __version__ without importing."""
    for line in open(fname):
        if line.startswith('__version__'):
            return f'{eval(line[13:].rstrip())}'


setuptools.setup(
    name                          = "matrix-py",
    version                       =  getversion("src/matrixpy.py"),
    description                   = "matrix-py module to add, substract, multiply matrices.",
    long_description              =  long_description,
    long_description_content_type = "text/markdown",
    author                        = "Fares Ahmed",
    author_email                  = "faresahmed@zohomail.com",
    python_requires               = ">=3.1",
    url                           = "https://github.com/FaresAhmedb/matrix-py",
    entry_points                  = {
        "console_scripts": ["matrixpy=matrixpy:main"],
    },
    install_requires              = ["setuptools"],
    include_package_data          =  True,
    package_dir                   = {"": "src"},
    py_modules                    = ["matrixpy"],
    zip_safe                      =  True,
    license                       = "GPLv2",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    )
