import click
import os
import subprocess
import re
import time
import json
import operator
import sys
import locale

from functools import reduce
from collections import defaultdict

def group_by(key, seq):
    return dict(reduce(lambda grp, val: grp[key(val)].append(val) or grp, seq, defaultdict(list)))

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

def findall(regexp, s):
    return [m.groupdict() for m in re.finditer(regexp, s)]

def parse_stream_filters(filter, default_action='-'):
    filters = findall(r'(?P<type>[vas])(?P<action>\+|\-)(?P<text>\w+)', filter)
    filters = group_by(operator.itemgetter('type'), filters)

    actions_per_type = {t: set(f['action'] for f in fs) for t,fs in filters.items()}
    if any(1 for _,a in actions_per_type.items() if len(a) > 1):
        click.secho('You can use only one filter action type (+ or -) per stream type!', fg='red', err=True)
        sys.exit(1)
    actions_per_type = {t: list(f)[0] for t,f in actions_per_type.items()}
    
    def _filter(stream_type, language):
        stream_type_id = stream_type[:1]
        action = actions_per_type.get(stream_type_id, default_action)
        if action == '-':
            for f in filters.get(stream_type_id, []):
                if f['text'] == language: return False
            return True
        else:
            for f in filters.get(stream_type_id, []):
                if f['text'] == language: return True
            return False
    return _filter
    

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
        fn = fn.encode(locale.getpreferredencoding())
        r = subprocess.check_output(FFPROBE_CMD + [fn], stderr=subprocess.STDOUT)
        return json.loads(r.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        return {'error': str(e.output)}
    return {}


def escape_csv(s):
    if '"' or "," in s:
        return '"%s"' % s.replace('"', '""')
    return s

def escape_cmd(s):
    return '"%s"' % s if ' ' in s else s

def format_seconds(s):
    d = '%.2f' % (s % 1)
    return time.strftime(r'%H:%M:%S', time.gmtime(s)) + d.lstrip('0')

extract_formats = {
  'hdmv_pgs_subtitle': 'sup',
  'subrip': 'srt',
  'aac': 'aac',
  'opus': 'opus'
}

@click.command(help='FFMPEG stream operations')
@click.argument('input', type=click.Path(exists=True), default='.')
@click.option('-f', '--filters', default='', help='Filter streams by language (eg. "s+eng a-ger")')
@click.option('--print-output', is_flag=True, help='Print ffmpeg commands')
@click.option('--apply', is_flag=True, help='Run conversion')
@click.option('--force-stereo', is_flag=True, help="Convert 5.1 audio streams to stereo")
@click.option('-c:a', 'acodec', type=click.Choice(['mp3', 'aac', 'opus']), help="Audio codec")
@click.option('-b:a', 'abitrate', type=str, help="Audio bitrate", default='96k')
@click.option('--hevc', is_flag=True, help='Convert video to HEVC')
@click.option('--crf', default=28, help='Sets quality when converting video (default for HEVC 28)')
def ffsel(input, filters, print_output, apply, force_stereo, acodec, abitrate, hevc, crf):
    files = [f for f in os.listdir(input) if os.path.isfile(f) and not f.startswith('.')] if os.path.isdir(input) else [input]
    
    stream_filter = parse_stream_filters(filters)
    output = []
    
    for f in files:
        cmd = ['ffmpeg', '-i', f, '-c', 'copy']
        
        probe = ffprobe(f)
        if not print_output:
            click.secho(f, bold=True, nl=False)
            click.secho(' (%s)' % sizeof_fmt(get_in(probe, 'format', 'size') or 0), fg='yellow')
        if not get_in(probe, 'streams'): continue
        
        output_stream_counter = defaultdict(lambda: -1)
        for s in get_in(probe, 'streams'):
            s_type = get_in(s, 'codec_type')
            s_info = ''
            if s_type == 'video':
                s_info = '%sx%s' % (get_in(s, 'width'), get_in(s, 'height'))
            elif s_type == 'audio':
                s_info = '%s' % (get_in(s, 'channel_layout'),)
            if get_in(s, 'disposition', 'default'):
                s_info = (s_info + ' default').strip()
            s_index = get_in(s, 'index')
            s_codec = get_in(s, 'codec_name')
            s_lang = sget_in(s, 'tags', 'language')
            
            keep = stream_filter(s_type, s_lang)
            t = ('  ' if keep else ' -') + '%i %s %s %s %s' % (s_index, s_type, s_codec, s_info, s_lang)
            if not print_output:
                click.secho(t, fg=('white' if keep else 'red'))
            if keep:
                cmd += ['-map', '0:%i'%s_index]
                output_stream_counter[s_type] += 1
                if force_stereo and s_type == 'audio' and get_in(s, 'channel_layout') not in ('stereo', 'mono'):
                    cmd += [
                      '-filter:a:%i' % output_stream_counter[s_type],
                      'pan=stereo|FL < 1.0*FL + 0.707*FC + 0.707*BL|FR < 1.0*FR + 0.707*FC + 0.707*BR'
                    ] if get_in(s, 'channel_layout') == '5.1' else [
                      '-ac:a:%i' % output_stream_counter[s_type],
                      '2'
                    ]
                    cmd += [
                      '-c:a:%i' % output_stream_counter[s_type], acodec or 'aac',
                      '-b:a:%i' % output_stream_counter[s_type], abitrate
                    ]
                elif acodec:
                    cmd += [
                      '-c:a:%i' % output_stream_counter[s_type], acodec or 'aac',
                      '-b:a:%i' % output_stream_counter[s_type], abitrate
                    ]
                if hevc and s_type == 'video':
                    cmd += [
                      '-c:v', 'libx265', 
                      '-crf', '%d' % crf,
                      '-preset', 'medium'
                    ]
        base, ext = os.path.splitext(f)
        cmd += ['out__%s%s' % (base, ext)]
        
        output_command = ' '.join((escape_cmd(c) for c in cmd))
        output += [output_command]
        if print_output:
            click.echo(output_command)

    if apply:
        confirmed = click.confirm('Do you want to continue?', abort=True)
        if confirmed:
            for cmd in output:
                os.system(cmd)

if __name__ == '__main__':
    ffsel()
