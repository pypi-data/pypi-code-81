#!/usr/bin/env python3

import unittest

import toc2audio


class title(unittest.TestCase):
    def test_title(self):
        md = 'This is the title\n\n[00:10] First\n\n[00:40] Second'
        toc = toc2audio.Toc(md)
        self.assertEqual(toc.title, 'This is the title')

    def test_single_word(self):
        md = 'Single!\n\n[00:10] First\n\n[00:40] Second'
        toc = toc2audio.Toc(md)
        self.assertEqual(toc.title, 'Single!')

    def test_markdown_header(self):
        md = '### Test title\n\n[00:10] First\n\n[00:40] Second'
        toc = toc2audio.Toc(md)
        self.assertEqual(toc.title, 'Test title')

    def test_markdown_header_strip(self):
        md = '###    \tTest title \t    \n\n[00:10] First\n\n[00:40] Second'
        toc = toc2audio.Toc(md)
        self.assertEqual(toc.title, 'Test title')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(title))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
