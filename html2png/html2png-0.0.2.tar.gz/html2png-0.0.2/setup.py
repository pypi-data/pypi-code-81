#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@metagriffin.net>
# date: 2021-04-13
# copy: (C) Copyright 2021-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import os, sys, setuptools
from setuptools import setup, find_packages

# require python 2.7+
if sys.hexversion < 0x02070000:
  raise RuntimeError('This package requires python 2.7 or better')

heredir = os.path.abspath(os.path.dirname(__file__))
def read(*parts, **kws):
  try:    return open(os.path.join(heredir, *parts)).read()
  except: return kws.get('default', '')

test_dependencies = [
  'nose                 >= 1.3.7',
  'coverage             >= 5.0.3',
  'fso                  >= 0.3.2',
]

dependencies = [
  'aadict               >= 0.2.3',
  'globre               >= 0.1.5',
  'six                  >= 1.14.0',
]

entrypoints = {
  'console_scripts': [
    'html2png           = html2png.cli:main',
  ],
}

classifiers = [
  'Development Status :: 1 - Planning',
  # 'Development Status :: 2 - Pre-Alpha',
  # 'Development Status :: 3 - Alpha',
  # 'Development Status :: 4 - Beta',
  # 'Development Status :: 5 - Production/Stable',
  'Environment :: Console',
  'Intended Audience :: End Users/Desktop',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Operating System :: OS Independent',
  'Natural Language :: English',
  'Topic :: Utilities',
  'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
]

setup(
  name                  = 'html2png',
  version               = read('VERSION.txt', default='0.0.1').strip(),
  description           = '',
  long_description      = read('README.rst'),
  classifiers           = classifiers,
  author                = 'metagriffin',
  author_email          = 'mg.pypi@metagriffin.net',
  url                   = 'http://github.com/metagriffin/html2png',
  keywords              = 'html rendering rasterizing qt5 web engine',
  packages              = find_packages(),
  platforms             = [ 'any' ],
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = dependencies,
  tests_require         = test_dependencies,
  test_suite            = 'html2png',
  entry_points          = entrypoints,
  license               = 'GPLv3+',
)

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
