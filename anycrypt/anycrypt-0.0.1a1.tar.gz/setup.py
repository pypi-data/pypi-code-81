#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This file is part of anycrypt.
#
#  anycrypt is an information encryption and decryption utility.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/anycrypt
#  Public Source Code Repository:
#    - https://source.codetrax.org/anycrypt
#
#  Copyright 2021 George Notaras <gnot@g-loaded.eu>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#  NOTES
#
#  Create source distribution tarball:
#    python setup.py sdist --formats=gztar
#
#  Create binary distribution rpm:
#    python setup.py bdist --formats=rpm
#
#  Create binary distribution rpm with being able to change an option:
#    python setup.py bdist_rpm --release 7
#
#  Test installation:
#    python setup.py install --prefix=/usr --root=/tmp
#
#  Install:
#    python setup.py install
#  Or:
#    python setup.py install --prefix=/usr
#



import sys
import os
sys.path.insert(0, os.path.abspath('src'))

from setuptools import setup

from anycrypt import get_version, get_status_classifier

def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if __name__=='__main__':
    setup(
        name = 'anycrypt',
        version = get_version(),
        license = 'GPLv2+',
        author = 'George Notaras',
        author_email = 'gnot@g-loaded.eu',
        maintainer = 'George Notaras',
        maintainer_email = 'gnot@g-loaded.eu',
        url = 'http://www.codetrax.org/projects/anycrypt',
        description = 'anycrypt is an information encryption and decryption utility.',
        long_description = read('README.rst'),
        download_url = 'https://source.codetrax.org/anycrypt',
        platforms=['any'],
        classifiers = [
            get_status_classifier(),
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: System',
        ],
        package_dir = {'': 'src'},
        packages = [
            'anycrypt',
        ],
        entry_points = {'console_scripts': [
            'anycrypt = anycrypt.main:main',
        ]},
        include_package_data = True,
        #zip_safe = False,
    )



