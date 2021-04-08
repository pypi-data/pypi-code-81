#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests of testing harness function in peyutil.test.support.struct_diff."""
import copy
import unittest

from peyutil.test.support.struct_diff import DictDiff, ListDiff
from peyutil.test.support import raise_http_error_with_more_detail


class TestRaiseHTTPErr(unittest.TestCase):
    """Unittest subclass for detection by harness."""

    def test_http_err(self):
        """Test of raise_http_error_with_more_detail."""
        # pylint: disable=attribute-defined-outside-init
        class DummyObj(object):
            """Dummy class."""
            def __init__(self):
                pass

            def __str__(self):
                return 'dummyobj str'
        x = DummyObj()
        x.response = DummyObj()
        x.response.text = 'hi'
        self.assertRaises(ValueError, raise_http_error_with_more_detail, x)
        try:
            raise_http_error_with_more_detail(x)
        except ValueError as o:
            self.assertEqual('dummyobj str, details: hi', str(o))


# noinspection PyTypeChecker
class TestDictDiff(unittest.TestCase):
    """Unittest subclass for detection by harness."""

    def test_equal_diff(self):
        """Test that identical dicts generate None from DictDiff.create."""
        a = {'some': ['dict'],
             'with': 'some',
             'key': {'s': 'that',
                     'are': ['nes', 'ted']}}
        b = dict(a)
        self.assertEqual(None, DictDiff.create(a, b))

    def test_add_del_diff(self):
        """Tests ability to detect the different keys sets."""
        a = {'some': ['dict'],
             'with': 'some',
             'key': {'s': 'that',
                     'are': ['nes', 'ted']}}
        b = dict(a)
        b['extra'] = 'cool stuff'
        ddo_a = DictDiff.create(a, b)
        add_str = ddo_a.additions_expr(par='obj')
        self.assertEqual(add_str, ["obj['extra'] = 'cool stuff'"])
        self.assertEqual([], ddo_a.deletions_expr(par='o'))
        self.assertEqual([], ddo_a.modification_expr(par='o'))
        ddo_d = DictDiff.create(b, a)
        add_str = ddo_d.deletions_expr(par='obj')
        self.assertEqual(add_str, ["del obj['extra']"])
        self.assertEqual([], ddo_d.additions_expr(par='o'))
        self.assertEqual([], ddo_d.modification_expr(par='o'))
        c_a = copy.deepcopy(a)
        self.assertEqual(a, c_a)
        c_b = copy.deepcopy(b)
        self.assertEqual(b, c_b)
        ddo_a.patch(c_a)
        self.assertEqual(b, c_a)
        ddo_d.patch(c_b)
        self.assertEqual(a, c_b)

    def test_add_mod_del_diff(self):
        """Tests ability to detect differing value for a key."""
        a = {'some': ['dict'],
             'with': 'some',
             'key': {'s': 'that',
                     'are': ['nes', 'ted']}}
        b = dict(a)
        b['extra'] = 'cool stuff'
        b['with'] = 'new stuff'
        del b['some']
        ddo_a = DictDiff.create(a, b)
        add_str = ddo_a.additions_expr(par='obj')
        self.assertEqual(add_str, ["obj['extra'] = 'cool stuff'"])
        self.assertEqual(["del obj['some']"], ddo_a.deletions_expr(par='obj'))
        self.assertEqual(["obj['with'] = 'new stuff'"], ddo_a.modification_expr(par='obj'))
        ddo_d = DictDiff.create(b, a)
        self.assertEqual(ddo_d.deletions_expr(par='obj'), ["del obj['extra']"])
        self.assertEqual(["obj['some'] = ['dict']"], ddo_d.additions_expr(par='obj'))
        self.assertEqual(["obj['with'] = 'some'"], ddo_d.modification_expr(par='obj'))
        c_a = copy.deepcopy(a)
        self.assertEqual(a, c_a)
        c_b = copy.deepcopy(b)
        self.assertEqual(b, c_b)
        ddo_a.patch(c_a)
        self.assertEqual(b, c_a)
        ddo_d.patch(c_b)
        self.assertEqual(a, c_b)

    def test_2nd_level_add_mod_del_diff(self):
        """Tests ability to detect differing nested object value."""
        a = {'some': ['dict'],
             'with': 'some',
             'key': {'s': 'that',
                     'are': ['nes', 'ted']}}
        b = copy.deepcopy(a)
        b['key']['a'] = 'cool stuff'
        b['key']['s'] = 'this'
        del b['key']['are']
        ddo_a = DictDiff.create(a, b)
        self.assertEqual(ddo_a.additions_expr(par='obj'), [])
        self.assertEqual([], ddo_a.deletions_expr(par='obj'))
        self.assertEqual(["obj['key']['a'] = 'cool stuff'",
                          "del obj['key']['are']",
                          "obj['key']['s'] = 'this'",
                          ], ddo_a.modification_expr(par='obj'))
        ddo_d = DictDiff.create(b, a)
        self.assertEqual(ddo_d.deletions_expr(par='obj'), [])
        self.assertEqual([], ddo_d.additions_expr(par='obj'))
        self.assertEqual(["obj['key']['are'] = ['nes', 'ted']",
                          "del obj['key']['a']",
                          "obj['key']['s'] = 'that'",
                          ], ddo_d.modification_expr(par='obj'))
        c_a = copy.deepcopy(a)
        self.assertEqual(a, c_a)
        c_b = copy.deepcopy(b)
        self.assertEqual(b, c_b)
        ddo_a.patch(c_a)
        self.assertEqual(b, c_a)
        ddo_d.patch(c_b)
        self.assertEqual(a, c_b)

    def test_list_add_mod_del_diff(self):
        """Tests ability to detect differing nested list object."""
        a = {'some': ['dict', 'bool'],
             'with': 'some',
             'key': {'s': 'that',
                     'are': ['nes', 'ted']}}
        b = copy.deepcopy(a)
        b['some'][0] = 'list'
        b['some'].append('last')
        ddo_a = DictDiff.create(a, b)
        self.assertEqual(ddo_a.additions_expr(par='obj'), [])
        self.assertEqual([], ddo_a.deletions_expr(par='obj'))
        self.assertEqual(["obj['some'][0] = 'list'",
                          "obj['some'].insert(2, 'last')"
                          ], ddo_a.modification_expr(par='obj'))
        ddo_d = DictDiff.create(b, a)
        self.assertEqual(ddo_d.deletions_expr(par='obj'), [])
        self.assertEqual([], ddo_d.additions_expr(par='obj'))
        self.assertEqual(["obj['some'][0] = 'dict'",
                          "obj['some'].pop(2)"
                          ], ddo_d.modification_expr(par='obj'))
        c_a = copy.deepcopy(a)
        self.assertEqual(a, c_a)
        c_b = copy.deepcopy(b)
        self.assertEqual(b, c_b)
        ddo_a.patch(c_a)
        self.assertEqual(b, c_a)
        ddo_d.patch(c_b)
        self.assertEqual(a, c_b)

    def test_wrap_dict_in_list(self):
        """Test of output when value changes from a list to a dict."""
        nd = {'some': 'nested'}
        a = {'some': ['dict', 'bool'],
             'with': nd,
             'key': {'s': 'that',
                     'are': ['nes', 'ted']}}
        b = copy.deepcopy(a)
        b['with'] = [copy.deepcopy(nd)]
        ddo_a = DictDiff.create(a, b, wrap_dict_in_list=True)
        self.assertEqual(ddo_a.additions_expr(par='obj'), [])
        self.assertEqual([], ddo_a.deletions_expr(par='obj'))
        self.assertEqual([], ddo_a.modification_expr(par='obj'))
        ddo_b = DictDiff.create(b, a, wrap_dict_in_list=True)
        self.assertEqual([], ddo_b.modification_expr(par='obj'))
        b['with'] = 4
        ddo_b = DictDiff.create(b, a, wrap_dict_in_list=True)
        self.assertEqual(["obj['with'] = {'some': 'nested'}"],
                         ddo_b.modification_expr(par='obj'))

    def test_list_diff(self):
        """Test of output when top level object is a list."""
        a = [0, 2, 3]
        self.assertIsNone(ListDiff.create(a, list(a)))
        b = [0, 1, 2, 3]
        ddo_a = ListDiff.create(a, b, wrap_dict_in_list=True)
        self.assertEqual(ddo_a.additions_expr(par='obj'), ['obj.insert(3, 3)'])
        self.assertEqual([], ddo_a.deletions_expr(par='obj'))
        self.assertEqual(['obj[1] = 1', 'obj[2] = 2'], ddo_a.modification_expr(par='obj'))


if __name__ == "__main__":
    unittest.main()
