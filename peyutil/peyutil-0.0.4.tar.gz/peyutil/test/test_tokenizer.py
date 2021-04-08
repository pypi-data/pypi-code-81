#! /usr/bin/env python
"""Tests of functions in peyutil.tokenizer."""
import unittest
from copy import deepcopy
import os
from peyutil.test.support.pathmap import get_test_path_mapper
from peyutil import write_to_filepath
from peyutil import (NewickTokenizer, NewickEvents, NewickEventFactory, StringIO)

path_map = get_test_path_mapper()
# pylint: disable=protected-access


class TestNewickTokenizer(unittest.TestCase):
    """Unittest subclass for detection by harness."""

    def test_no_arg(self):
        """Tests that NewickTokenizer without arg raises ValueError."""
        self.assertRaises(ValueError, NewickTokenizer)

    def test_no_start_open_parens(self):
        """Tests Newick must start with (."""
        self.assertRaises(ValueError, NewickTokenizer, newick='hi')

    def test_extra_suffix(self):
        """Tests Newick must end with ) or ;."""
        nt = NewickTokenizer(newick='(a,(b,c));suffix')
        self.assertRaises(ValueError, nt.tokens)

    def test_unclosed(self):
        """Tests Newick open parens are closed."""
        nt = NewickTokenizer(newick='(a,(b,c)')
        self.assertRaises(ValueError, nt.tokens)

    def test_extra_closed(self):
        """Tests Newick with extra close parens generate errors."""
        nt = NewickTokenizer(newick='(a,(b,c)));')
        self.assertRaises(ValueError, nt.tokens)

    def test_peek_none(self):
        """Tests behavior of peek when there are no more tokens."""
        nt = NewickTokenizer(newick='(a,(b,c));')
        nt.tokens()
        self.assertIsNone(nt._peek())

    def test_sans_comma(self):
        """Tests error with a comma is omitted."""
        nt = NewickTokenizer(newick='(a,(b,c)(d,e));')
        self.assertRaises(ValueError, nt.tokens)

    def test_unclosed_comment(self):
        """Tests that unclosed [] comments generate errors."""
        nt = NewickTokenizer(newick='(a,(b,c),[(d,e));')
        self.assertRaises(ValueError, nt.tokens)

    def test_comma_bef_semicolon(self):
        """Test that terminating ; is not preceded by ,."""
        nt = NewickTokenizer(newick='(a,(b,c),(d,e)),;')
        self.assertRaises(ValueError, nt.tokens)

    def test_unexpected_comma(self):
        """Test consecutive commas generate errors."""
        nt = NewickTokenizer(newick='(a,(b,c),,(d,e));')
        self.assertRaises(ValueError, nt.tokens)

    def test_label(self):
        """Test that unquoted labels with newline character generate errors."""
        nt = NewickTokenizer(newick="(a\n'b',(b,c),(d,e));")
        self.assertRaises(ValueError, nt.tokens)

    def test_quoted_edge_info(self):
        """Test that quoting edge info generates no error and string edge length."""
        exp = ['(', 'a', ',', '(', 'b', ',', 'c', ')', ':', '4', ',',
               '(', 'd', ',', 'e', ')', ')', ';']
        self._do_test("(a,(b,c):'4',(d,e));", exp)

    def test_open_closed(self):
        """Tests that () generates an error."""
        nt = NewickTokenizer(newick='(a,(),(d,e));')
        self.assertRaises(ValueError, nt.tokens)

    def test_simple(self):
        """Tests valid newick parsing, with tests that comments are skipped."""
        exp = ['(', '(', 'h', ',', 'p', ')', 'hp', ',', 'g', ')', 'hpg', ';']
        content = '((h,p)hp,g)hpg;'
        self._do_test(content, exp)
        content = '((h,p[test])hp,g)hpg;'
        self._do_test(content, exp)
        content = '  ( (  h , p[test] [test2])  hp,  g) hpg ;'
        self._do_test(content, exp)

    def test_quoted(self):
        """Tests valid newick parsing with quoted labels and comments."""
        exp = ['(', '(', 'h ', ',', 'p', ')', 'h p', ',', "g()[],':_", ')', 'hpg', ';']
        content = "((h_ ,'p')h p,'g()[],'':_')hpg;"
        self._do_test(content, exp)
        content = "(('h ',p)h p,'g()[],'':_')hpg;"
        self._do_test(content, exp)

    def _do_test(self, content, expected):
        """Part of the testing harness.

        Writes `content`, the parses and compares to `expected`.
        """
        self.assertEqual(list(NewickTokenizer(StringIO(content))), expected)
        self.assertEqual(list(NewickTokenizer(newick=content)), expected)
        fp = path_map.next_unique_scratch_filepath('tok_test')
        try:
            write_to_filepath(content, fp)
            self.assertEqual(list(NewickTokenizer(filepath=fp)), expected)
        finally:
            try:
                os.unlink(fp)
            except:  # pragma: no cover
                pass

    def test_odd_quotes(self):
        """Test that an odd # of single quotes generates an error."""
        content = "((h_ ,'p)h p,g()[],:_)hpg;"
        tok = NewickTokenizer(StringIO(content))
        self.assertRaises(Exception, tok.tokens)
        content = "((h_ ,'p')h p,'g()[]',:_')hpg;"
        tok = NewickTokenizer(StringIO(content))
        self.assertRaises(Exception, tok.tokens)

    def test_branch_length(self):
        """Test that edge length info can contain scientific notation."""
        exp = ['(', '(', 'h', ':', '4.0', ',', 'p', ':', '1.1461E-5', ')',
               'hp', ':', '1351.146436', ',', 'g', ')', 'hpg', ';']
        content = '((h:4.0,p:1.1461E-5)hp:1351.146436,g)hpg;'
        self._do_test(content, exp)


class TestNewickEvents(unittest.TestCase):
    """Unittest subclass for detection by harness."""

    def test_simple(self):
        """Test of NewickEvents from parsing of strings with and without comments."""
        exp = [{'type': NewickEvents.OPEN_SUBTREE, 'comments': []},
               {'type': NewickEvents.OPEN_SUBTREE, 'comments': []},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'h'},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'p'},
               {'edge_info': '1', 'type': NewickEvents.CLOSE_SUBTREE,
                'comments': [], 'label': 'hp'},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'g'},
               {'edge_info': None, 'type': NewickEvents.CLOSE_SUBTREE,
                'comments': [], 'label': 'hpg'}
               ]
        content = '((h,p)hp:1,g)hpg;'
        self._do_test(content, exp)
        content = '((h,[pretest]p[test][posttest])hp,g)hpg;'
        exp = [{'type': NewickEvents.OPEN_SUBTREE, 'comments': []},
               {'type': NewickEvents.OPEN_SUBTREE, 'comments': []},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'h'},
               {'edge_info': None, 'type': NewickEvents.TIP,
                'comments': ['pretest', 'test', 'posttest'], 'label': 'p'},
               {'edge_info': None, 'type': NewickEvents.CLOSE_SUBTREE,
                'comments': [], 'label': 'hp'},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'g'},
               {'edge_info': None, 'type': NewickEvents.CLOSE_SUBTREE,
                'comments': [], 'label': 'hpg'}
               ]
        self._do_test(content, exp)

    def test_no_arg(self):
        """Tests that NewickEventFactory without arg raises ValueError."""
        self.assertRaises(ValueError, NewickEventFactory)

    def _do_test(self, content, expected):
        """Part of the testing harness.

        Writes `content`, the parses and compares to `expected`.
        """
        nt = NewickTokenizer(stream=StringIO(content))
        e = [deepcopy(i) for i in NewickEventFactory(tokenizer=nt)]
        self.assertEqual(e, expected)
        new_e = []

        def append_to_new_e(event):
            new_e.append(deepcopy(event))

        NewickEventFactory(newick=content, event_handler=append_to_new_e)
        self.assertEqual(new_e, expected)


if __name__ == "__main__":
    unittest.main()
