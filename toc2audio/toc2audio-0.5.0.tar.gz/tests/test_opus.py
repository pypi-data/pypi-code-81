#!/usr/bin/env python3

import unittest
import pathlib
import tempfile
import shutil
import re

import mutagen
import mutagen.oggopus


import toc2audio


class ogg(unittest.TestCase):
    expr = re.compile('^CHAPTER[0-9][0-9][0-9]$')

    def setUp(self):
        self.set_filetype()
        self.tmp_dir_obj = tempfile.TemporaryDirectory()
        self.tmp_dir = pathlib.Path(self.tmp_dir_obj.name)
        self.tmp_file = self.tmp_dir / ('test' + self.suffix)
        shutil.copyfile('silence' + self.suffix, self.tmp_file)

    def tearDown(self):
        self.tmp_dir_obj.cleanup()

    def test_chapters(self):
        md = '[00:10] First\n\n[00:40] Second'
        toc = toc2audio.Toc(md)
        self.tagger(self.tmp_file, toc, add_chapters=True)
        metadata = self.metadata(self.tmp_file)

        chapters = [i for i, j in metadata.tags if self.expr.match(i)]
        self.assertEqual(len(chapters), 2)

        for i, v in enumerate(((10, 40, 'First'), (40, 86440, 'Second'))):
            start_time, end_time, title = v
            chapter = f'CHAPTER{i:03}'
            start_time = f'00:00:{start_time}.000'
            self.assertEqual(metadata.tags[chapter], [start_time])
            self.assertEqual(metadata.tags[chapter+'NAME'], [title])

    def test_previous_chapters(self):
        md = '[00:10] First\n\n[00:40] Second'
        toc = toc2audio.Toc(md)
        self.tagger(self.tmp_file, toc, add_chapters=True)

        md = '[00:23] Third'
        toc = toc2audio.Toc(md)
        self.tagger(self.tmp_file, toc, add_chapters=True)

        metadata = self.metadata(self.tmp_file)

        chapters = [i for i, j in metadata.tags if self.expr.match(i)]
        self.assertEqual(len(chapters), 1)
        self.assertEqual(metadata.tags['CHAPTER000'], ['00:00:23.000'])
        self.assertEqual(metadata.tags['CHAPTER000NAME'], ['Third'])

    def test_advertisement(self):
        md = '[00:10] First'
        toc = toc2audio.Toc(md)
        self.tagger(self.tmp_file, toc, add_chapters=True)
        metadata = self.metadata(self.tmp_file)
        version = f'toc2audio {toc2audio.__version__} - '
        version += 'https://docs.jcea.es/toc2audio/'
        self.assertEqual(metadata.tags.get('_TAGGER'), [version])


class opus(ogg):
    def set_filetype(self):
        self.suffix = '.opus'
        self.tagger = toc2audio.add_tags_opus
        self.metadata = mutagen.oggopus.OggOpus


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(opus))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
