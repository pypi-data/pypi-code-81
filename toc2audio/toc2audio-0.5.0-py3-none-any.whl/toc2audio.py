#!/usr/bin/env python3

"""Add Table of Contents and chapters to audio files"""

__version__ = '0.5.0'

import argparse
import pathlib
import tempfile
import os
import webbrowser
import xml.etree.ElementTree as etree
import functools
import xml.etree.ElementTree
import subprocess
import re
import sys

import markdown
import mutagen
import mutagen.id3
import mutagen.oggopus
import mutagen.oggvorbis


@functools.total_ordering
class Offset:
    def __init__(self, hours=0, minutes=0, seconds=0, compact=True):
        self.compact = compact
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds

    def __repr__(self):
        return self.pprint()

    def pprint(self, compact=None):
        if not self._hours:
            if compact is None:
                compact = self.compact
            if compact:
                return f'{self._minutes:02d}:{self._seconds:02d}'
        return f'{self._hours:02d}:{self._minutes:02d}:{self._seconds:02d}'

    def add(self, seconds, compact=None):
        if compact is None:
            compact = self.compact
        offset, seconds = divmod(self._seconds + seconds, 60)
        offset, minutes = divmod(self._minutes + offset, 60)
        hours = self._hours + offset
        return type(self)(hours, minutes, seconds, compact=compact)

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
    def from_seconds(cls, seconds, compact=True):
        return cls(compact=compact).add(seconds)


class Timestamps(markdown.inlinepatterns.InlineProcessor):
    # Beside default value, explicing "offset" takes it out of
    # both "args" and "kwargs". Useful when calling "super()__init__()".
    def __init__(self, *args, offset=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = offset

    def handleMatch(self, m, data):
        hour = m.group('hours')
        compact = hour is None
        hour = 0 if hour is None else int(hour)
        timestamp = Offset(hours=hour,
                           minutes=int(m.group('minutes')),
                           seconds=int(m.group('seconds')),
                           compact=compact)
        timestamp = timestamp.add(self.offset)
        ts = timestamp.to_seconds()
        # We can not simply set "text" because in a Element tree,
        # any text in a tag goes BEFORE any tag child.
        # https://docs.python.org/3/library/
        #         xml.etree.elementtree.html#xml.etree.ElementTree.Element.text

        attrib = {
                    'ts': str(ts),
                    'compact': str(int(timestamp.compact)),
                    'offset': str(self.offset),
                 }
        el = etree.Element('timestamp', attrib=attrib)
        el2 = etree.Element('strong')
        # To avoid infinite recursion, "[]" reintroduced at postprocessing
        el2.text = f'[!*!{timestamp.pprint()}]'
        el3 = etree.Element('topic')
        el3.text = data[m.end(0):]
        el.extend((el2, el3))
        return el, m.start(0), len(data)


class TimestampsExtension(markdown.extensions.Extension):
    # Beside default value, explicing "offset" takes it out of
    # both "args" and "kwargs". Useful when calling "super()__init__()".
    def __init__(self, *args, offset=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = offset

    def extendMarkdown(self, md):
        pattern = (r'(\[((?P<hours>[0-9]?[0-9]):|)'
                   r'(?P<minutes>[0-9]?[0-9]):(?P<seconds>[0-9][0-9])\])')
        md.inlinePatterns.register(Timestamps(pattern, md, offset=self.offset),
                                   'timestamps', 10000)


class Toc:
    def __init__(self, file, offset=0):
        if isinstance(file, pathlib.Path):
            file = file.read_text(encoding='utf-8')

        self.text = file

        md = markdown.Markdown(extensions=[TimestampsExtension(offset=offset)])
        self.html = md.convert(self.text).replace('[!*!', '[')

        # We get the timestamps as a postprocessing step instead of doing it
        # while parsing the markdown because the markdown parse "direction"
        # can vary even in the same document when you have enumerations, etc.

        document = f'<?xml version="1.0"?><XXXX>{self.html}</XXXX>'
        root = xml.etree.ElementTree.fromstring(document)
        timestamps = []
        last = Offset().add(-1)  # Negative number is API *ABUSE*!
        for timestamp in root.findall('.//timestamp'):
            compact = bool(int(timestamp.get('compact')))
            offset = Offset(compact=compact).add(int(timestamp.get('ts')))
            if last >= offset:
                raise ValueError('Non monotonic timestamps: '
                                 f'{last} > {offset}')
            last = offset
            topic = timestamp.find('topic')
            topic = ''.join(topic.itertext()).strip()
            topic = topic.replace('\r', ' ').replace('\n', ' ')
            topic = topic.replace('\t', ' ')
            while True:
                topic2 = topic.replace('  ', ' ')
                if topic == topic2:
                    break
                topic = topic2

            timestamps.append((offset, topic))

        # XXX: We don't know the duration of the audio, so
        # the last chapter is set to 24 hours long.
        timestamps.append((timestamps[-1][0].add(24 * 60 * 60), 'DUMMY'))
        timestamps = [(ts[0], timestamps[i + 1][0], ts[1])
                      for i, ts in enumerate(timestamps[:-1])]
        self.timestamps = timestamps


def show_in_browser(toc, msg=None):
    fd, tmpname = tempfile.mkstemp(suffix='.html')
    print()
    print(toc.html)
    print()
    try:
        html = '<html><head><meta charset="utf-8"/></head><body>'
        html = f'{html}{toc.html}</body></html>'
        os.write(fd, html.encode('utf-8'))
        os.close(fd)
        webbrowser.open('file://' + tmpname)

        if msg:
            print(msg, file=sys.stderr)
        print('Press ENTER to continue', file=sys.stderr)
        input()
    finally:
        os.unlink(tmpname)


# https://medium.com/@dathanbennett/
#             adding-chapters-to-an-mp4-file-using-ffmpeg-5e43df269687
#
# https://ffmpeg.org/ffmpeg-formats.html#Metadata-1

def add_tags_mp4(path, toc, add_toc=False, add_chapters=False):
    version = f'toc2audio {__version__} - https://docs.jcea.es/toc2audio/'
    if add_chapters:
        metadata = ';FFMETADATA1\n'
        for ts_start, ts_end, title in toc.timestamps:
            metadata += '\n[CHAPTER]\nTIMEBASE=1/1000\n'
            metadata += f'START={ts_start.to_seconds()*1000}\n'
            metadata += f'END={ts_end.to_seconds()*1000}\n'
            metadata += f'title={title}\n'

            path_out = path.with_name(path.name + '2')

        try:
            # XXX: Improvements in Python 3.7
            r = subprocess.run(['ffmpeg', '-i', path, '-i', '-',
                                '-map_metadata', '0', '-map_chapters', '1',
                                '-codec', 'copy', '-f', 'mp4',
                                path_out],
                               input=metadata, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True)
            if r.returncode:
                print(r.stdout)
                print(r.stderr)
                r.check_returncode()

            audio = mutagen.mp4.MP4(path_out)
            audio.tags['\xa9too'] = audio.tags.get('\xa9too', []) + [version]
            audio.save()

            path_out.rename(path)
        finally:
            # XXX: Improvement in Python 3.8
            if path_out.exists():
                path_out.unlink()


def add_tags_ogg(ogg, toc, add_toc=False, add_chapters=False):
    version = f'toc2audio {__version__} - https://docs.jcea.es/toc2audio/'
    if add_chapters:
        re_chapters = re.compile('^chapter[0-9][0-9][0-9]')
        tags = ogg.tags.keys()
        for tag in tags:
            if re_chapters.match(tag):
                del ogg.tags[tag]

        for i, (ts_start, ts_end, title) in enumerate(toc.timestamps):
            chapter = f'CHAPTER{i:03}'
            ogg.tags[chapter] = f'{ts_start.pprint(compact=False)}.000'
            ogg.tags[chapter+'NAME'] = title
        ogg.tags['_TAGGER'] = version
        ogg.save()


def add_tags_opus(path, toc, add_toc=False, add_chapters=False):
    ogg = mutagen.oggopus.OggOpus(path)
    return add_tags_ogg(ogg, toc, add_toc=add_toc, add_chapters=add_chapters)


def add_tags_vorbis(path, toc, add_toc=False, add_chapters=False):
    ogg = mutagen.oggvorbis.OggVorbis(path)
    return add_tags_ogg(ogg, toc, add_toc=add_toc, add_chapters=add_chapters)


def add_tags_mp3(path, toc, add_toc=False, add_chapters=False):
    version = f'toc2audio {__version__} - https://docs.jcea.es/toc2audio/'
    try:
        tags = mutagen.id3.ID3(path)
    except mutagen.id3.ID3NoHeaderError:
        tags = mutagen.id3.ID3()

    title = tags.get('TIT2', '')
    if title:
        title = title.text

    if add_chapters:
        # Delete existing TOC
        ctoc = tags.get('CTOC:toc')
        if ctoc:
            for i in ctoc.child_element_ids:
                del tags[f'CHAP:{i}']
            del tags['CTOC:toc']

        # XXX: Change this
        title = mutagen.id3.TIT2(text=title)
        chapters = [f'chp{i}' for i in range(1, len(toc.timestamps) + 1)]
        tags.add(
            mutagen.id3.CTOC(element_id='toc',
                             flags=(mutagen.id3.CTOCFlags.TOP_LEVEL |
                                    mutagen.id3.CTOCFlags.ORDERED),
                             child_element_ids=chapters,
                             sub_frames=[title]))
        for n, (start_ts, end_ts, title) in enumerate(toc.timestamps, 1):
            title = mutagen.id3.TIT2(text=[title])
            tags.add(mutagen.id3.CHAP(element_id=f'chp{n}',
                                      start_time=start_ts.to_seconds(),
                                      end_time=end_ts.to_seconds(),
                                      sub_frames=[title]))
        tags.add(mutagen.id3.TXXX(desc='tagger', text=[version],
                                  encoding=mutagen.id3.Encoding.UTF8))
        tags.save(path)


def add_tags_audio(audios, toc, add_toc, add_chapters):
    if add_toc:
        raise NotImplementedError('Adding TOC to audio not supported yet')

    for path in audios:
        suffix = path.suffix.lower()
        if suffix == '.mp3':
            add_tags_mp3(path, toc, add_toc, add_chapters)
        elif suffix == '.m4a':
            add_tags_mp4(path, toc, add_toc, add_chapters)
        elif suffix == '.opus':
            add_tags_opus(path, toc, add_toc, add_chapters)
        elif suffix == '.ogg':
            add_tags_vorbis(path, toc, add_toc, add_chapters)
        else:
            raise TypeError(f'Unrecognized extension: {str(path)}')


def main():
    parser = argparse.ArgumentParser(
            description='Add Table of Contents and chapters to audio files')
    parser.add_argument('--version', action='store_true',
                        help='Show version info')
    parser.add_argument('--offset', nargs=1,
                        help='Seconds or [HH:]MM:SS to add to ALL timestamps')
    parser.add_argument('--show', action='store_true',
                        help='Show the generated HTML in your browser')
    parser.add_argument('--toc', action='store_true',
                        help='Store Table of Contents in the audio file')
    parser.add_argument('--chapters', action='store_true',
                        help='Store chapters details in the audio file')
    parser.add_argument('TOC', nargs='?',
                        help='Table of Contents file')
    parser.add_argument('AUDIO', nargs='*', type=pathlib.Path,
                        help='Audio file')

    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit()
    offset = args.offset
    if offset is None:
        offset = 0
    else:
        value = offset[0]
        if ':' in value:
            offset = 0
            for n in value.split(':'):
                offset = offset * 60 + int(n)
        else:
            offset = int(value)

    toc = args.TOC
    if toc is None:
        parser.error('TOC argument required')

    if args.toc:
        parser.error('"--toc" parameter is not YET supported')

    if (args.toc or args.chapters) and (not args.AUDIO):
        # XXX: Undocumented
        parser.error('AUDIO arguments required')

    toc = Toc(pathlib.Path(toc), offset=offset)
    offset_hh_mm_ss = Offset().add(offset).pprint()
    msg = (f'We applied an offset of {offset} seconds ({offset_hh_mm_ss}) '
           'to all timestamps')

    if args.show:
        show_in_browser(toc, msg=msg)
    else:
        print(msg, file=sys.stderr)

    if args.toc or args.chapters:
        add_tags_audio(args.AUDIO, toc,
                       add_toc=args.toc, add_chapters=args.chapters)

    if args.chapters:
        print()
        print('Chapters:')
        for start_ts, end_ts, title in toc.timestamps:
            print(f'{start_ts} - {end_ts}: {title}')


if __name__ == '__main__':
    main()
