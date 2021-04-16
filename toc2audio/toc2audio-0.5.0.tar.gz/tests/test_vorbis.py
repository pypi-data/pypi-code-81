#!/usr/bin/env python3

import unittest

import mutagen
import mutagen.oggvorbis


import toc2audio
import test_opus


class vorbis(test_opus.ogg):
    def set_filetype(self):
        self.suffix = '.ogg'
        self.tagger = toc2audio.add_tags_vorbis
        self.metadata = mutagen.oggvorbis.OggVorbis


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(vorbis))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
