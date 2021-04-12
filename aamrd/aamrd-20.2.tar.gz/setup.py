# -*- python -*-
#
# Copyright (C) 2014-2016 Liang Chen
# Copyright (C) 2016-2021 Xingeng Chen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import find_packages, setup


class PkgSetup(object):
    NAME = 'aamrd'
    DESCRIB = 'job scheduler'
    LICENSE = 'GNU Affero General Public License'
    AUTHOR = 'Xingeng Chen'

    CLASSIFIERS = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]

    KEYWORDS = ('Scheduler',)

    @classmethod
    def read_src_file(cls, *parts):
        import codecs
        import os
        dir_path = os.path.abspath(os.path.dirname(__file__))
        with codecs.open(os.path.join(dir_path, *parts), 'r') as _f:
            return _f.read()

    @classmethod
    def find_version(cls, *file_paths):
        import re

        MSG_VERSION_STRING_NOTFOUND = 'Unable to find version string.'

        version_file = cls.read_src_file(*file_paths)
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError(MSG_VERSION_STRING_NOTFOUND)

    @classmethod
    def getConfig(cls):
        cfg = {
            'name': cls.NAME,
            'author': cls.AUTHOR,
            'license': cls.LICENSE,
            'classifiers': cls.CLASSIFIERS,
            'keywords': cls.KEYWORDS,
            'version': cls.find_version(cls.NAME, '__init__.py'),
            'packages': find_packages(),
            'platforms': 'Any',
            'python_requires': '>=2.7',
            'install_requires': ['dmprj',],
            'tests_require': ['flake8', 'pytest'],
            'description': cls.DESCRIB,
            'long_description': cls.read_src_file('README.md'),
            'long_description_content_type': 'text/markdown',
        }
        return cfg


setup(**(PkgSetup.getConfig()))
