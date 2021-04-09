#!/usr/bin/env python3

import unittest
import random

import toc2audio


class timestamps(unittest.TestCase):
    def test_deteccion(self):
        for ts in ('0:56', '4:56', '34:56', '0:34:56', '7:34:56'):
            md = f'Title\n\n[{ts}] prueba'
            toc = toc2audio.Toc(md)
            ts = toc.timestamps
            self.assertEqual(len(ts), 1, ts)
            self.assertIsInstance(ts[0][0], toc2audio.Offset, ts[0])
            self.assertEqual(ts[0][1], 'prueba', ts)

    def test_completo(self):
        rnd = random.Random()
        rnd.seed(1234567890)
        text = ['Title']
        offset = toc2audio.Offset()
        for i in range(100):
            text.append(f'[{offset}] Prueba de tiempo = {offset.to_seconds()}')
            offset = offset.add(seconds=rnd.randrange(100, 1000))
        md = '\n\n'.join(text)
        toc = toc2audio.Toc(md)
        self.assertEqual(len(toc.timestamps), 100)
        last = -1
        for t in toc.timestamps:
            ts, txt = t
            txt = txt.split()
            self.assertEqual(txt[:4], ['Prueba', 'de', 'tiempo', '='], t)
            seconds = ts.to_seconds()
            self.assertEqual(seconds, int(txt[-1]), t)
            self.assertGreater(seconds, last, t)
            last = seconds

    def test_non_monotonic(self):
        md = 'Title\n\n[00:24] first\n\n[1:23] Second'
        toc2audio.Toc(md)  # Should work

        md = '[01:23] first\n\n[0:24] Second'
        with self.assertRaises(ValueError):
            toc2audio.Toc(md)

    def test_monotonic_lists(self):
        md = """
# First line will be the title of the TOC (header marks removed)

* [00:50] Presentation

    Here I describe the topics we will talk about.

* [02:11] Topic 1

    Blah blah blah blah...

* [17:29] Topic 2

    Blah blah blah blah...
    """.strip()

        toc2audio.Toc(md)  # Should work

    def test_comparison_types(self):
        offset = toc2audio.Offset()
        with self.assertRaises(TypeError):
            offset < 5
        with self.assertRaises(TypeError):
            offset == 5

    def test_comparison(self):
        offset = toc2audio.Offset()
        offset2 = toc2audio.Offset(seconds=10)
        self.assertGreater(offset2, offset)
        self.assertGreaterEqual(offset2, offset)
        self.assertLess(offset, offset2)
        self.assertLessEqual(offset, offset2)
        self.assertNotEqual(offset, offset2)

        offset = offset.add(10)
        self.assertGreaterEqual(offset2, offset)
        self.assertLessEqual(offset, offset2)
        self.assertEqual(offset, offset2)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(timestamps))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
