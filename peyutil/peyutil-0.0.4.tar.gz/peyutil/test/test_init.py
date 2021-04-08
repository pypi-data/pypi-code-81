#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests of functions in peyutil.__init__.py."""
import unittest
import tempfile
import time
import os
from peyutil import (any_early_exit,
                     doi2url,
                     get_unique_filepath,
                     pretty_timestamp,
                     propinquity_fn_to_study_tree, )


class TestInit(unittest.TestCase):
    """Unittest subclass for detection by harness."""

    def test_any_early_exit(self):
        """Test of any_early_exit."""
        v = [1, 2, 3]
        self.assertFalse(any_early_exit(v, lambda x: x > 20))
        self.assertTrue(any_early_exit(v, lambda x: x > 2))
        self.assertTrue(any_early_exit(v, lambda x: x < 2))

        def raise_if_gt2(x):
            if x > 2:
                raise ValueError('np')
            return True

        self.assertTrue(any_early_exit(v, lambda x: raise_if_gt2(x) and x < 2))
        self.assertTrue(any_early_exit(v, lambda x: True and x > 2))
        self.assertRaises(ValueError, any_early_exit, v, lambda x: raise_if_gt2(x) and x > 2)

    def test_pretty_timestamp(self):
        """Test of pretty_timestamp."""
        t = time.gmtime(1500000678)
        self.assertEqual('2017-07-14', pretty_timestamp(t))
        self.assertEqual('2017-07-14', pretty_timestamp(t, 0))
        self.assertEqual('20170714025118', pretty_timestamp(t, 1))
        self.assertEqual('14-07-2017', pretty_timestamp(t, '%d-%m-%Y'))
        # Warning: these next 2 tests are gonna break starting Jan-01-2100
        self.assertTrue(pretty_timestamp(style=1).startswith('20'))
        import datetime
        now = datetime.datetime.now()
        self.assertTrue('+20' in pretty_timestamp(now, '+%Y'))

    def test_doi2url(self):
        """Test of doi2url."""
        x = '10.1071/IS12017'
        exp = 'http://dx.doi.org/10.1071/IS12017'
        self.assertEqual(exp, doi2url(x))
        self.assertEqual(exp, doi2url(exp))
        self.assertEqual(exp, doi2url('doi: {}'.format(x)))
        self.assertEqual(exp, doi2url('doi:{}'.format(x)))
        self.assertEqual('http://gibberish', doi2url('gibberish'))

    def test_get_uniq_fp(self):
        """Test of get_unique_filepath."""
        try:
            tdf = tempfile.TemporaryDirectory
        except:  # pragma: no cover
            # Skip this test on Python2.7. just feeling lazy...
            return
        with tdf() as fd:
            stem = os.path.join(fd, 'ufp')
            ufp1 = get_unique_filepath(stem)
            ufp2 = get_unique_filepath(stem)
            self.assertEqual(ufp1, ufp2)
            with open(ufp1, 'w'):
                ufp3 = get_unique_filepath(stem)
                self.assertNotEqual(ufp1, ufp3)
                with open(ufp3, 'w'):
                    ufp4 = get_unique_filepath(stem)
                    self.assertNotEqual(ufp1, ufp4)
                    self.assertNotEqual(ufp3, ufp4)

    def test_unpack_propinquity_fn(self):
        """Test of propinquity_fn_to_study_tree."""
        x = 'ot_982@tree4.json'
        self.assertEqual(propinquity_fn_to_study_tree(x), ['ot_982', 'tree4'])
        self.assertEqual(propinquity_fn_to_study_tree(x, False), ['ot_982', 'tree4.json'])
        self.assertRaises(ValueError, propinquity_fn_to_study_tree, 'noAtsymbol.json')
        self.assertRaises(ValueError, propinquity_fn_to_study_tree, 'two@sym@.json')


if __name__ == "__main__":
    unittest.main()
