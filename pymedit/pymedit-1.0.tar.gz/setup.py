# Copyright 2018-2020 CNRS, Ecole Polytechnique and Safran.
#
# This file is part of pymedit.
#
# pymedit is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pymedit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# A copy of the GNU General Public License is included below.
# For further information, see <http://www.gnu.org/licenses/>.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymedit",
    version="1.0",
    author="Florian Feppon",
    author_email="florian.feppon@polytechnique.edu",
    license="GNU GPL version 3",
    description="Package pymedit for operating on 2D and 3D meshes in the INRIA" \
    " mesh format",
    keywords="pymedit, mesh",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/florian.feppon/pymedit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    install_requires=['numpy>=1.12.1',
                      'scipy>=0.19.1',
                      'cvxopt>=1.2.1',
                      'colored>=1.3.93',
                      'matplotlib>=2.0.2'
                      ],
    python_requires='>=3.6',
)
