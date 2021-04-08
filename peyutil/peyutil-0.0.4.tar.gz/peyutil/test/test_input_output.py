#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests of functions from peyutil.input_output."""
import unittest
import tempfile
import os

from peyutil.test.support.pathmap import get_test_path_mapper

from peyutil import (expand_path,
                     open_for_group_write,
                     parse_study_tree_list,
                     pretty_dict_str,
                     read_as_json,
                     read_filepath,
                     write_as_json,
                     write_pretty_dict_str,
                     write_to_filepath,)


path_map = get_test_path_mapper()


class TestIO(unittest.TestCase):
    """Unittest subclass for detection by harness."""

    def test_expand_path(self):
        """Tests of the `expand_path` function."""
        os.environ['BOGUS'] = 'somebogus'
        expy = os.path.join('somebogus', 'path')
        self.assertEqual(expand_path('${BOGUS}/path'), expy)
        inp = '~/${BOGUS}/path'
        y = expand_path(inp)
        self.assertTrue(y.endswith(expy))
        self.assertFalse(y.startswith('~'))

    def test_parse_study_tree_list_nojson(self):
        """Tests of text form of `parse_study_tree_list` function."""
        stl = path_map.nexson_source_path('not_really_nexson.txt')
        x = parse_study_tree_list(stl)
        exp = [{'study_id': 'pg_10', 'tree_id': 'tree2'},
               {'study_id': 'ot_11', 'tree_id': 'tree1'},
               {'study_id': 'ot_12', 'tree_id': 'tree3'}]
        self.assertEqual(x, exp)

    def test_parse_study_tree_list(self):
        """Tests of JSON form of `parse_study_tree_list` function."""
        stl = path_map.nexson_source_path('study_tree_list.json')
        x = parse_study_tree_list(stl)
        exp = [{'study_id': 'pg_1', 'tree_id': 'tree2'}, {'study_id': 'pg_2', 'tree_id': 'tree3'}]
        self.assertEqual(x, exp)
        aj = read_as_json(stl)
        self.assertEqual(aj, exp)
        raw = '''[
  {"study_id":  "pg_1", "tree_id": "tree2"},
  {"study_id":  "pg_2", "tree_id": "tree3"}
]'''
        self.assertEqual(raw, read_filepath(stl))
        self.assertEqual(raw, read_filepath(stl, encoding='utf-8'))
        z = '''{
  "study_id": "pg_1",
  "tree_id": "tree2"
}'''
        self.assertEqual(z, pretty_dict_str(exp[0]))
        try:
            tdf = tempfile.TemporaryDirectory
        except:  # pragma: no cover
            # Skip this test on Python2.7. just feeling lazy...
            return
        noindentraw = '''[
{
"study_id": "pg_1",
"tree_id": "tree2"
},
{
"study_id": "pg_2",
"tree_id": "tree3"
}
]
'''
        with tdf() as tmpdir:
            tfp = os.path.join(tmpdir, 'x.json')
            write_as_json(exp, tfp)
            self.assertEqual(noindentraw, read_filepath(tfp))
            ufp = os.path.join(tmpdir, 'y.json')
            with open_for_group_write(ufp, 'w') as outst:
                write_as_json(exp, outst)
            self.assertEqual(noindentraw, read_filepath(ufp))
            rtfp = os.path.join(tmpdir, 'raw.txt')
            write_to_filepath(noindentraw, rtfp)
            self.assertEqual(noindentraw, read_filepath(rtfp))
            # with subdir
            pdfp = os.path.join(tmpdir, 'subdir', 'prettydictfp')
            with open_for_group_write(pdfp, 'w') as gro:
                write_pretty_dict_str(gro, exp[0])
            self.assertEqual(z, read_filepath(pdfp))

            # without subdir
            pdfp = os.path.join(tmpdir, 'prettydictfp')
            with open_for_group_write(pdfp, 'w') as gro:
                write_pretty_dict_str(gro, exp[0])
            self.assertEqual(z, read_filepath(pdfp))
            # using write_to_filepath and subdir2
            pdfp = os.path.join(tmpdir, 'subdir2', 'prettydictfp')
            write_to_filepath(pretty_dict_str(exp[0]), pdfp, group_writeable=True)
            self.assertEqual(z, read_filepath(pdfp))


if __name__ == "__main__":
    unittest.main()
