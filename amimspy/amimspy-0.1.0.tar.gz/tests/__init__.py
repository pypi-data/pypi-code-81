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


import unittest


def suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.', pattern='test_*.py')
    return test_suite
