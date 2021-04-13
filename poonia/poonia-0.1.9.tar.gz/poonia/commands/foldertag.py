#!/usr/bin/python3
import click
import subprocess
import json
import os
import re
from functools import reduce
import locale

FFPROBE_CMD = 'ffprobe -hide_banner -loglevel fatal -show_error -show_format -show_streams -show_programs -show_chapters -show_private_data -print_format json'.split(' ')
def ffprobe(fn):
    try:
        fn = fn.encode(locale.getpreferredencoding())
        r = subprocess.check_output(FFPROBE_CMD + [fn], stderr=subprocess.STDOUT)
        return json.loads(r.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        return {'error': str(e.output)}
    return {}

def get_tags(fn):
    probe = ffprobe(fn)
    tags = probe.get('format', {}).get('tags', {})
    return {k.lower(): v for k,v in tags.items()}

MEDIA_EXTENSIONS = {'.aac', '.alac', '.aif', '.aifc', '.aiff', '.dsf', '.flac', '.mka', '.mkv', '.ape', '.mp3', '.mp4', '.m4a', '.m4b', '.m4v', '.mpc', '.ogg', '.opus', '.wma', '.wv', '.wav'}
def is_media_file(fn):
    _, ext = os.path.splitext(fn)
    return ext.lower() in MEDIA_EXTENSIONS

def equal_keys(d1, d2):
    return dict(set(d1.items()).intersection(set(d2.items())))

def format_str(tpl, kv):
    def sub(m):
        k = m.group(1).lower()
        if not k in kv:
            raise Exception("'%s' not found in source tags. Could not interpolate the template '%s'" % (k, tpl))
        return kv[k]
    return re.sub('%(.+?)%', sub, tpl)

def print_tags(d):
    for k,v in d.items():
        click.secho(k, nl=False, fg='yellow')
        click.echo(": '%s'" % v)

def add_custom_tags(d):
    if d.get('date', None):
        m = re.findall('(\d{4})', d.get('date'))
        if m: d['year'] = m[0]
    if d.get('album_artist', None) and not d.get('artist', None):
        d['artist'] = d['album_artist']

def show_rename_msg(src, dst, apply=False):
    click.secho("'%s'" % src, bold=True, fg='green', nl=False)
    click.secho(" has been renamed to " if apply else ' will be renamed to ', nl=False)
    click.secho("'%s'" % dst, fg='green', bold=True)

def safe_filename(s):
    s = re.sub('\w(: +)', ' - ', s)
    for c in '/\\:': s = s.replace(c, '-')
    s = s.replace('"', "'")
    for c in '?<>|*': s = s.replace(c, '_')
    return s.strip()

@click.command(help='Rename folder based on media tags of files it contains')
@click.argument('directories', type=click.Path(exists=True), nargs=-1)
@click.option('-t', '--template', default=r'%artist% [%year%] - %album%', help='Template for directory name')
@click.option('--tags', is_flag=True, help='Show available tags')
@click.option('--apply', is_flag=True, help='Apply changes')
def foldertag(directories, template, tags, apply):
    for directory in directories:
        directory = os.path.normpath(directory)
        if not os.path.isdir(directory):
            click.secho("'%s' is not a directory" % directory, fg='red')
            continue
        # files = [os.path.join(directory, f) for f in os.listdir(directory)]
        files = [os.path.join(dp, f) for dp, dn, fn in os.walk(directory) for f in fn]
        files = [f for f in files if os.path.isfile(f) and is_media_file(f)]
        file_tags = []
        for f in files:
            try:
                file_tags.append(get_tags(f))
            except Exception as e:
                click.secho("'%s': " % f, fg='yellow', nl=False)
                click.secho(str(e), fg='red')
                continue
        if not file_tags:
            click.secho("'%s' contains no music files" % directory, fg='red')
            continue
        common_tags = reduce(equal_keys, file_tags)
        add_custom_tags(common_tags)
        if tags:
            print_tags(common_tags)
            click.echo()
        
        basename = os.path.basename(directory)
        try:
            target_name = safe_filename(format_str(template, common_tags))
        except Exception as e:
            click.secho("'%s': " % directory, fg='yellow', nl=False)
            click.secho(str(e), fg='red')
            continue
        if basename == target_name:
            click.secho("'%s'" % basename, bold=True, fg='green', nl=False)
            click.secho(" adheres to provided template")
            continue
        show_rename_msg(basename, target_name, apply)
        if apply:
            os.rename(directory, target_name)

if __name__ == '__main__':
    foldertag()