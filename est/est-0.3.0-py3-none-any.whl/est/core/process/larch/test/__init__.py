# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ############################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "07/25/2019"

import unittest

from .test_autobk import suite as test_autobk_suite
from .test_mback import suite as test_mback_suite
from .test_mback_norm import suite as test_mback_norm_suite
from .test_pre_edge import suite as test_pre_edge_suite
from .test_workflow import suite as test_workflow_suite
from .test_xftf import suite as test_xftf_suite


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_autobk_suite())
    test_suite.addTest(test_mback_suite())
    test_suite.addTest(test_mback_norm_suite())
    test_suite.addTest(test_pre_edge_suite())
    test_suite.addTest(test_workflow_suite())
    test_suite.addTest(test_xftf_suite())
    return test_suite
