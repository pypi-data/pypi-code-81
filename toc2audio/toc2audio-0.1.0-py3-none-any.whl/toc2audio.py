#!/usr/bin/env python3

"""Add Table of Contents and chapters to audio files"""

__version__ = '0.1.0'

import argparse
import pathlib
import tempfile
import os
import webbrowser
import xml.etree.ElementTree as etree
import functools
import xml.etree.ElementTree

import markdown
import mutagen
import mutagen.id3


@functools.total_ordering
class Offset:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds

    def __repr__(self):
        return f'{self._hours:02d}:{self._minutes:02d}:{self._seconds:02d}'

    def add(self, seconds):
        offset, seconds = divmod(self._seconds + seconds, 60)
        offset, minutes = divmod(self._minutes + offset, 60)
        hours = self._hours + offset
        return type(self)(hours, minutes, seconds)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError('Incompatible types')
        return self.to_seconds() == other.to_seconds()

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError('Incompatible types')
        return self.to_seconds() < other.to_seconds()

    def to_seconds(self):
        return self._hours * 3600 + self._minutes * 60 + self._seconds

    @classmethod
    def from_seconds(cls, seconds):
        return cls().add(seconds)


class Timestamps(markdown.inlinepatterns.InlineProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handleMatch(self, m, data):
        hour = m.group('hours')
        hour = 0 if hour is None else int(hour)
        timestamp = Offset(hours=hour,
                           minutes=int(m.group('minutes')),
                           seconds=int(m.group('seconds')))
        ts = timestamp.to_seconds()
        # We can not simply set "text" because in a Element tree,
        # any text in a tag goes BEFORE any tag child.
        # https://docs.python.org/3/library/
        #         xml.etree.elementtree.html#xml.etree.ElementTree.Element.text

        el = etree.Element('timestamp', attrib={'ts': str(ts)})
        el2 = etree.Element('strong')
        # To avoid infinite recursion, "[]" reintroduced at postprocessing
        el2.text = f'[!*!{m.group(1)[1:]}'
        el3 = etree.Element('topic')
        el3.text = data[m.end(0):]
        el.extend((el2, el3))
        return el, m.start(0), len(data)


class TimestampsExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        pattern = (r'(\[((?P<hours>[0-9]?[0-9]):|)'
                   r'(?P<minutes>[0-9]?[0-9]):(?P<seconds>[0-9][0-9])\])')
        md.inlinePatterns.register(Timestamps(pattern, md),
                                   'timestamps', 10000)


class Toc:
    def __init__(self, file):
        if isinstance(file, pathlib.Path):
            file = file.read_text(encoding='utf-8')

        self.text = file

        title = self.text.split(sep='\n', maxsplit=1)[0]
        while title[0] == '#':
            title = title[1:]
        self.title = title.strip()

        md = markdown.Markdown(extensions=[TimestampsExtension()])
        self.html = md.convert(self.text).replace('[!*!', '[')

        # We get the timestamps as a postprocessing step instead of doing it
        # while parsing the markdown because the markdown parse "direction"
        # can vary even in the same document when you have enumerations, etc.

        document = f'<?xml version="1.0"?><XXXX>{self.html}</XXXX>'
        root = xml.etree.ElementTree.fromstring(document)
        self.timestamps = []
        last = Offset().add(-1)  # Negative number is API *ABUSE*!
        for timestamp in root.findall('.//timestamp'):
            offset = Offset().add(int(timestamp.get('ts')))
            if last >= offset:
                raise ValueError('Non monotonic timestamps: '
                                 f'{last} > {offset}')
            last = offset
            topic = timestamp.find('topic').text.strip()
            self.timestamps.append((offset, topic))


def show_in_browser(toc):
    fd, tmpname = tempfile.mkstemp(suffix='.html')
    try:
        html = '<html><head><meta charset="utf-8"/></head><body>'
        html = f'{html}{toc.html}</body></html>'
        os.write(fd, html.encode('utf-8'))
        os.close(fd)
        webbrowser.open('file://' + tmpname)
        print('Press ENTER to continue')
        input()
    finally:
        os.unlink(tmpname)


def add_tags_mp3(path, toc, add_toc=False, add_chapters=False):
    try:
        tags = mutagen.id3.ID3(path)

        # Delete existing TOC
        ctoc = tags.get('CTOC:toc')
        if ctoc:
            for i in ctoc.child_element_ids:
                del tags[f'CHAP:{i}']
            del tags['CTOC:toc']
    except mutagen.id3.ID3NoHeaderError:
        tags = mutagen.id3.ID3()

    if add_chapters:
        # XXX: Change this
        title = mutagen.id3.TIT2(text=[toc.title])
        chapters = [f'chp{i}' for i in range(1, len(toc.timestamps) + 1)]
        tags.add(
            mutagen.id3.CTOC(element_id='toc',
                             flags=(mutagen.id3.CTOCFlags.TOP_LEVEL |
                                    mutagen.id3.CTOCFlags.ORDERED),
                             child_element_ids=chapters,
                             sub_frames=[title]))
        for n, (start_ts, title) in enumerate(toc.timestamps, 1):
            if n < len(toc.timestamps):
                end_ts = toc.timestamps[n][0]
            else:
                # XXX: We don't know the duration of the audio, so
                # the last chapter is set to 24 hours long.
                end_ts = toc.timestamps[n - 1][0].add(24 * 60 * 60)

            title = mutagen.id3.TIT2(text=[title])
            tags.add(mutagen.id3.CHAP(element_id=f'chp{n}',
                                      start_time=start_ts.to_seconds(),
                                      end_time=end_ts.to_seconds(),
                                      sub_frames=[title]))
    tags.save(path)


def add_tags_audio(audios, toc, add_toc, add_chapters):
    if add_toc:
        raise NotImplementedError('Adding TOC to audio not supported yet')

    for path in audios:
        suffix = path.suffix.lower()
        if suffix == '.mp3':
            add_tags_mp3(path, toc, add_toc, add_chapters)
        # elif suffix == '.m4a':
        #     add_tags_m4a(path, toc, add_toc, add_chapters)
        # elif suffix == '.opus':
        #     add_tags_opus(path, toc, add_toc, add_chapters)
        else:
            raise TypeError(f'Unrecognized extension: {str(path)}')


def main():
    parser = argparse.ArgumentParser(
            description='Add Table of Contents and chapters to audio files')
    parser.add_argument('--show', action='store_true',
                        help='Show the generated HTML in your browser')
    parser.add_argument('--toc', action='store_true',
                        help='Store Table of Contents in the audio file')
    parser.add_argument('--chapters', action='store_true',
                        help='Store chapters details in the audio file')
    parser.add_argument('TOC', nargs=1,
                        help='Table of Contents file')
    parser.add_argument('AUDIO', nargs='*', type=pathlib.Path,
                        help='Audio file')

    args = parser.parse_args()
    if (args.toc or args.chapters) and (not args.AUDIO):
        # XXX: Undocumented
        parser.error('AUDIO arguments required')
    toc = args.TOC[0]

    toc = Toc(pathlib.Path(toc))

    if args.show:
        show_in_browser(toc)

    if args.toc or args.chapters:
        add_tags_audio(args.AUDIO, toc,
                       add_toc=args.toc, add_chapters=args.chapters)


if __name__ == '__main__':
    main()
