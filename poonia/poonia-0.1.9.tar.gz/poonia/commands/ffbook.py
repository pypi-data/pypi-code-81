import click
import os
import subprocess
import re
import time
import json
import operator
import sys

from functools import reduce
from collections import defaultdict

# ffmpeg -i INPUT -f ffmetadata FFMETADATAFILE
# ffmpeg -i INPUT -i FFMETADATAFILE -map_metadata 1 -codec copy OUTPUT


def get_in(obj, *keys):
    for k in keys:
        v = obj.get(k, None)
        if v is None:
            return None
        obj = v
    return obj

def sget_in(obj, *keys):
    r = get_in(obj, *keys)
    if r is None: return ''
    return str(r)

def sizeof_fmt(num, suffix='B'):
    num = float(num)
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

FFPROBE_CMD = 'ffprobe -hide_banner -loglevel fatal -show_error -show_format -show_streams -show_programs -show_chapters -show_private_data -print_format json'.split(' ')
def ffprobe(fn):
    try:
        r = subprocess.check_output(FFPROBE_CMD + [fn], stderr=subprocess.STDOUT)
        return json.loads(str(r))
    except subprocess.CalledProcessError as e:
        return {'error': str(e.output)}
    return {}

def read_audio(fn):
    r = subprocess.check_output(['ffmpeg', '-i', fn, '-f', 'u16le', '-ar', '48000', '-ac', '1', '-'], stderr=None)
    return bytes(r)

def escape_cmd(s):
    return '"%s"' % s if ' ' in s else s

def format_seconds(s):
    d = '%.3f' % (s % 1)
    return time.strftime(r'%H:%M:%S', time.gmtime(s)) + d.lstrip('01')

@click.command(help='FFMPEG audiobook tool')
@click.argument('input', type=click.Path(exists=True, dir_okay=False, readable=True), nargs=-1)
@click.option('--cover', type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option('--metadata', type=click.Choice(['full', 'no-chapters', 'none']), default='full')
@click.option('--bitrate', '-b', default='24k')
def ffbook(input, cover, metadata, bitrate):
    probes = [ffprobe(f) for f in input]
    #click.echo(probes)
    
    if not probes:
        click.secho('No files to process!', fg='red', err=True)
        sys.exit(1)
    
    title = sget_in(probes[0], 'format', 'tags', 'title')
    artist = sget_in(probes[0], 'format', 'tags', 'artist')
    album_artist = sget_in(probes[0], 'format', 'tags', 'album_artist')
    album = sget_in(probes[0], 'format', 'tags', 'album')

    durations = [float(get_in(p, 'format', 'duration')) for p in probes]
    chapter_marks = [sum(durations[:i]) for i in range(len(durations))]
    chapters = []
    for i, p in enumerate(probes):
      duration = float(get_in(p, 'format', 'duration'))
      
      click.secho('%s ' % sget_in(p, 'format', 'filename'), bold=True, nl=False)
      click.secho('%s ' % format_seconds(duration), fg='yellow', nl=False)
      click.secho('%s ' % sizeof_fmt(get_in(p, 'format', 'size')), fg='cyan', nl=False)
      
      if metadata == 'full':
          chapter = ('Chapter %d' % (i+1), format_seconds(chapter_marks[i]))
          chapters += [chapter]
          click.echo('[%s | %s]' % chapter, nl=False)
      click.echo()
      
    confirmed = click.confirm('Do you want to continue?', abort=True)
    if confirmed:
        pcm_filename = '__output.pcm'
        metadata_filename = '__metadata_ogg.txt'
        ogg_filename = '__ogg.opus'
        output_filename = '_book.mka'
        
        if metadata != 'none':
            with open(metadata_filename, 'wb') as f:
                f.write(''';FFMETADATA1
title=%s
artist=%s
album_artist=%s
album=%s
''' % (title, artist, album_artist, album))
                if metadata == 'full':
                    for i, ch in enumerate(chapters, 1):
                        f.write('CHAPTER%02d=%s\n' % (i, ch[1]))
                        f.write('CHAPTER%02dNAME=%s\n' % (i, ch[0]))
        
        with open(pcm_filename, 'wb') as f:
            for i, p in enumerate(probes):
                x = read_audio(sget_in(p, 'format', 'filename'))
                f.write(x)

        subprocess.check_output([
          'ffmpeg', '-f', 'u16le', '-ar', '48000', '-ac', '1',
          '-i', pcm_filename
        ] + (['-i', metadata_filename, '-map_metadata', '1'] if metadata != 'none' else []) + [
          '-b:a', bitrate, '-c:a', 'libopus', ogg_filename
        ], stderr=None)
        
        subprocess.check_output([
          'ffmpeg', '-i', ogg_filename
        ] + ([
          '-attach', cover, '-metadata:s', 'mimetype=image/jpeg', '-metadata:s', 'filename=book-cover.jpg'
        ] if cover else []) + ['-c:a', 'copy', output_filename], stderr=None)


if __name__ == '__main__':
    ffbook()
