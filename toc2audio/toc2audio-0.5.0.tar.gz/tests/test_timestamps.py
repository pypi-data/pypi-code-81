#!/usr/bin/env python3

import unittest
import random

import toc2audio


class timestamps(unittest.TestCase):
    def test_deteccion(self):
        for ts in ('0:56', '4:56', '34:56', '0:34:56', '7:34:56'):
            md = f'[{ts}] prueba'
            toc = toc2audio.Toc(md)
            ts = toc.timestamps
            self.assertEqual(len(ts), 1, ts)
            self.assertIsInstance(ts[0][0], toc2audio.Offset, ts[0])
            self.assertIsInstance(ts[0][1], toc2audio.Offset, ts[0])
            self.assertEqual(ts[0][2], 'prueba', ts)

    def test_completo(self):
        rnd = random.Random()
        rnd.seed(1234567890)
        text = []
        offset = toc2audio.Offset()
        for i in range(100):
            text.append(f'[{offset}] Prueba de tiempo = {offset.to_seconds()}')
            offset = offset.add(seconds=rnd.randrange(100, 1000))

        md = '\n\n'.join(text)
        toc = toc2audio.Toc(md)
        self.assertEqual(len(toc.timestamps), 100)
        last = -1
        end_previous = toc.timestamps[0][0]
        for t in toc.timestamps:
            ts_start, ts_end, txt = t
            txt = txt.split()
            self.assertEqual(txt[:4], ['Prueba', 'de', 'tiempo', '='], t)
            self.assertEqual(ts_start, end_previous)
            seconds = ts_start.to_seconds()
            self.assertEqual(seconds, int(txt[-1]), t)
            self.assertGreater(seconds, last, t)
            last = seconds
            end_previous = ts_end

    def test_compact_basic(self):
        offset = toc2audio.Offset(compact=False)
        self.assertEqual(offset.pprint(), '00:00:00')
        self.assertEqual(offset.pprint(compact=False), '00:00:00')
        self.assertEqual(offset.pprint(compact=True), '00:00')

        offset = toc2audio.Offset(compact=True)
        self.assertEqual(offset.pprint(), '00:00')
        self.assertEqual(offset.pprint(compact=False), '00:00:00')
        self.assertEqual(offset.pprint(compact=True), '00:00')

        offset = toc2audio.Offset()
        # Compact by default
        self.assertEqual(offset.pprint(), '00:00')
        self.assertEqual(offset.pprint(compact=False), '00:00:00')
        self.assertEqual(offset.pprint(compact=True), '00:00')

        offset = toc2audio.Offset(minutes=53, seconds=11)
        # Compact by default
        self.assertEqual(offset.pprint(), '53:11')
        self.assertEqual(offset.pprint(compact=False), '00:53:11')
        self.assertEqual(offset.pprint(compact=True), '53:11')

    def test_compact_add(self):
        offset = toc2audio.Offset(minutes=58, seconds=31)
        # Compact by default
        self.assertEqual(offset.pprint(), '58:31')
        self.assertEqual(offset.pprint(compact=False), '00:58:31')
        self.assertEqual(offset.pprint(compact=True), '58:31')

        offset2 = offset.add(seconds=7)
        # Keep parent compact preference
        self.assertEqual(offset2.pprint(), '58:38')
        self.assertEqual(offset2.pprint(compact=False), '00:58:38')
        self.assertEqual(offset2.pprint(compact=True), '58:38')

        # New preference
        offset2 = offset.add(seconds=7, compact=True)
        self.assertEqual(offset2.pprint(), '58:38')
        self.assertEqual(offset2.pprint(compact=False), '00:58:38')
        self.assertEqual(offset2.pprint(compact=True), '58:38')

        # New preference
        offset2 = offset.add(seconds=7, compact=False)
        self.assertEqual(offset2.pprint(), '00:58:38')
        self.assertEqual(offset2.pprint(compact=False), '00:58:38')
        self.assertEqual(offset2.pprint(compact=True), '58:38')

        offset3 = offset2.add(seconds=1)
        # Keep parent compact preference
        self.assertEqual(offset3.pprint(), '00:58:39')
        self.assertEqual(offset3.pprint(compact=False), '00:58:39')
        self.assertEqual(offset3.pprint(compact=True), '58:39')

        offset2 = offset.add(seconds=60 * 60)
        # Keep parent compact preference
        self.assertEqual(offset2.pprint(), '01:58:31')
        self.assertEqual(offset2.pprint(compact=False), '01:58:31')
        self.assertEqual(offset2.pprint(compact=True), '01:58:31')

    def test_compact_from_seconds(self):
        offset = toc2audio.Offset.from_seconds(seconds=947)
        self.assertEqual(offset.pprint(), '15:47')

        offset = toc2audio.Offset.from_seconds(seconds=947, compact=False)
        self.assertEqual(offset.pprint(), '00:15:47')

        offset = toc2audio.Offset.from_seconds(seconds=7199)
        self.assertEqual(offset.pprint(), '01:59:59')

        offset = toc2audio.Offset.from_seconds(seconds=7199, compact=True)
        self.assertEqual(offset.pprint(), '01:59:59')

    def test_compact_preserve(self):
        md = '[00:17:24] Non Compact\n\n[21:26] Compact'
        toc = toc2audio.Toc(md)
        self.assertEqual(toc.timestamps[0][0].pprint(), '00:17:24')
        self.assertEqual(toc.timestamps[1][0].pprint(), '21:26')

    def test_compact_preserve_with_offset(self):
        md = '[00:17:24] Non Compact\n\n[21:26] Compact'
        toc = toc2audio.Toc(md, offset=71)
        self.assertEqual(toc.timestamps[0][0].pprint(), '00:18:35')
        self.assertEqual(toc.timestamps[1][0].pprint(), '22:37')

        toc = toc2audio.Toc(md, offset=7270)
        self.assertEqual(toc.timestamps[0][0].pprint(), '02:18:34')
        self.assertEqual(toc.timestamps[1][0].pprint(), '02:22:36')

    def test_drop_html_tags(self):
        md = '[00:24] First <https://www.jcea.es/> second   '
        toc = toc2audio.Toc(md)
        self.assertEqual(toc.timestamps[0][2],
                         'First https://www.jcea.es/ second')

        md = '[00:24] First <b>second   </b>'
        toc = toc2audio.Toc(md)
        self.assertEqual(toc.timestamps[0][2], 'First second')

    def test_lines_and_multiple_spaces(self):
        md = '[00:24] First\tXX \n    second   '
        toc = toc2audio.Toc(md)
        self.assertEqual(toc.timestamps[0][2], 'First XX second')

    def test_non_monotonic(self):
        md = '[00:24] first\n\n[1:23] Second'
        toc2audio.Toc(md)  # Should work

        md = '[01:23] first\n\n[0:24] Second'
        with self.assertRaises(ValueError):
            toc2audio.Toc(md)

    def test_monotonic_lists(self):
        md = """
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
