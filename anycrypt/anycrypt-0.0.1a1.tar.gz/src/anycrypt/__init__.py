# -*- coding: utf-8 -*-
#
#  This file is part of anycrypt.
#
#  anycrypt is an information encryption and decryption utility.
#
#  Development Web Site:
#    - https://www.codetrax.org/projects/anycrypt
#  Public Source Code Repository:
#    - https://source.codetrax.org/gnotaras/anycrypt
#
#  Copyright 2021 George Notaras <gnot@g-loaded.eu>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.
#

# Scheme: <major>.<minor>.<maintenance>.<maturity>.<revision>
# maturity: final/beta/alpha

VERSION = (0, 0, 1, 'alpha', 1)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2] is not None:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3] != 'final':
        if VERSION[4] > 0:
            version = '%s%s%s' % (version, VERSION[3][0], VERSION[4])
        else:
            version = '%s%s' % (version, VERSION[3][0])
    return version

__version__ = get_version()

def get_status_classifier():
    if VERSION[3] == 'final':
        return 'Development Status :: 5 - Production/Stable'
    elif VERSION[3] == 'beta':
        return 'Development Status :: 4 - Beta'
    elif VERSION[3] == 'alpha':
        return 'Development Status :: 3 - Alpha'
    raise NotImplementedError

