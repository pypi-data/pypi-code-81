#!/usr/bin/env python3

import unittest
import pathlib
import tempfile
import shutil

import mutagen
import mutagen.id3

import toc2audio


class mp3(unittest.TestCase):
    def setUp(self):
        self.tmp_dir_obj = tempfile.TemporaryDirectory()
        self.tmp_dir = pathlib.Path(self.tmp_dir_obj.name)
        self.tmp_file = self.tmp_dir / 'test.mp3'
        shutil.copyfile('silence.mp3', self.tmp_file)

    def tearDown(self):
        self.tmp_dir_obj.cleanup()

    def test_chapters(self):
        md = '[00:10] First\n\n[00:40] Second'
        toc = toc2audio.Toc(md)
        toc2audio.add_tags_mp3(self.tmp_file, toc, add_chapters=True)
        tags = mutagen.id3.ID3(self.tmp_file)
        ctoc = tags['CTOC:toc']
        self.assertEqual(ctoc.child_element_ids, ['chp1', 'chp2'])
        self.assertFalse('TIT2' in ctoc.sub_frames)
        for i, v in enumerate(((10, 40, 'First'), (40, 86440, 'Second')), 1):
            start_time, end_time, title = v
            chap = tags[f'CHAP:chp{i}']
            self.assertEqual(chap.start_time, start_time)
            self.assertEqual(chap.end_time, end_time)
            self.assertEqual(chap.sub_frames['TIT2'], title)

    def test_previous_chapters(self):
        md = '[00:10] First\n\n[00:40] Second'
        toc = toc2audio.Toc(md)
        toc2audio.add_tags_mp3(self.tmp_file, toc, add_chapters=True)

        md = '[00:23] Third'
        toc = toc2audio.Toc(md)
        toc2audio.add_tags_mp3(self.tmp_file, toc, add_chapters=True)

        tags = mutagen.id3.ID3(self.tmp_file)
        self.assertEqual(tags['CTOC:toc'].child_element_ids, ['chp1'])
        self.assertFalse('TIT2' in tags['CTOC:toc'].sub_frames)
        chap = tags['CHAP:chp1']
        self.assertEqual(chap.start_time, 23)
        self.assertEqual(chap.end_time, 86400 + 23)
        self.assertEqual(chap.sub_frames['TIT2'], 'Third')
        self.assertFalse('CHAP:chp2' in tags)

    def test_toc_title(self):
        audio = mutagen.id3.ID3()
        audio.add(mutagen.id3.TIT2(text='The title'))
        audio.save(self.tmp_file)

        md = '[00:23] First'
        toc = toc2audio.Toc(md)
        toc2audio.add_tags_mp3(self.tmp_file, toc, add_chapters=True)

        tags = mutagen.id3.ID3(self.tmp_file)
        self.assertEqual(tags['CTOC:toc'].sub_frames['TIT2'], 'The title')

    def test_toc_title_overwrite(self):
        audio = mutagen.id3.ID3()
        audio.add(mutagen.id3.TIT2(text='This is the title'))
        audio.save(self.tmp_file)

        md = '[00:23] First'
        toc = toc2audio.Toc(md)
        toc2audio.add_tags_mp3(self.tmp_file, toc, add_chapters=True)

        audio = mutagen.id3.ID3(self.tmp_file)
        audio['TIT2'] = mutagen.id3.TIT2(text='New title')
        audio.save()

        toc2audio.add_tags_mp3(self.tmp_file, toc, add_chapters=True)

        tags = mutagen.id3.ID3(self.tmp_file)
        self.assertEqual(tags['CTOC:toc'].sub_frames['TIT2'], 'New title')

    def test_advertisement(self):
        md = '[00:10] First'
        toc = toc2audio.Toc(md)
        toc2audio.add_tags_mp3(self.tmp_file, toc, add_chapters=True)
        tags = mutagen.id3.ID3(self.tmp_file)
        version = f'toc2audio {toc2audio.__version__} - '
        version += 'https://docs.jcea.es/toc2audio/'
        self.assertIn(version, tags.get('TXXX:tagger'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(mp3))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
