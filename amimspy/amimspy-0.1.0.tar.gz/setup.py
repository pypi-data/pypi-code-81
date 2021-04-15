#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020-2021 Matthew Smith, Ralf Weber
#
# This file is part of AMIMSpy.
#
# AMIMSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AMIMSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AMIMSpy.  If not, see <https://www.gnu.org/licenses/>.
#


import amimspy

import setuptools


def main():

    setuptools.setup(name="amimspy",
        version=amimspy.__version__,
        description="Python package for processing acoustic mist ionization mass spectrometry-based metabolomics and lipidomics data",
        long_description=open('README.rst').read(),
        long_description_content_type="text/x-rst",
        author="Matthew Smith, Ralf Weber",
        author_email="mjs708@student.bham.ac.uk, r.j.weber@bham.ac.uk",
        url="https://github.com/computational-metabolomics/amimspy",
        license="GPLv3",
        platforms=['Windows, UNIX'],
        keywords=['Metabolomics', 'Lipidomics', 'Mass spectrometry', 'Data Processing', 'Acoustic mist ionization mass spectrometry', 'Direct-Infusion Mass Spectrometry'],
        packages=setuptools.find_packages(),
        test_suite='tests.suite',
        python_requires='>=3.7',
        install_requires=open('requirements.txt').read().splitlines(),
        include_package_data=True,
        project_urls={
            "Documentation": "https://amimspy.readthedocs.io/en/latest/",
            "Changelog": "https://amimspy.readthedocs.io/en/latest/changelog.html",
            "Bug Tracker": "https://github.com/computational-metabolomics/amimspy/issues",
        },
        classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Topic :: Scientific/Engineering :: Bio-Informatics",
          "Topic :: Scientific/Engineering :: Chemistry",
          "Topic :: Utilities",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
        ],
        entry_points={
         'console_scripts': [
             'amimspy = amimspy.__main__:main'
         ]
        }
    )


if __name__ == "__main__":
    main()
