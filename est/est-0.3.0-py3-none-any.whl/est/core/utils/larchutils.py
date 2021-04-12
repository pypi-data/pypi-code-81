# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
# ###########################################################################*/
"""Define some utils relative to larch"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "02/12/2019"


from larch.symboltable import Group


def group_to_dict(group):
    """Convert the larch group to a serializable dictionary

    :param group: the group to convert to a serializable dictionary
    :type: larch.symboltable.Group
    :returns: dictionary corresponding to the given larch.symboltable.Group
    :rtype: dictionary
    """
    res = {}
    for key in group._members():
        if isinstance(group._members()[key], Group):
            res[key] = group_to_dict(group._members()[key])
        else:
            res[key] = group._members()[key]


def dict_to_group(dict_, group):
    """Update the given larch group with the content of the dictionary

    :param dict_:
    :type: dict
    :param group:
    :type: larch.symboltable.Group
    """
    for key in dict_:
        group._members()[key] = dict_[key]
