import click
import os
import subprocess
import re
import time

h = lambda data: hashlib.sha1(data).hexdigest()
avg = lambda lst: sum(lst) / float(len(lst))

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def ffmpeg_info(fn):
    try:
        r = subprocess.check_output(["ffmpeg", "-i", fn], stderr=subprocess.STDOUT)
        return str(r)
    except subprocess.CalledProcessError as e:
        return str(e.output)
    return ''

def media_length(fn):
    o = ffmpeg_info(fn)
    durations = re.findall('Duration: ([\d:.]+)', o)
    if not durations:
        return None
    fst_duration = durations[0]
    parts = zip(
        (int(p) for p in re.findall('\d+', fst_duration)[::-1]),
        [.01, 1, 60, 60**2]
    )
    return fst_duration, sum(p[0] * p[1] for p in parts)

def escape_csv(s):
    if '"' or "," in s:
        return '"%s"' % s.replace('"', '""')
    return s

def format_seconds(s):
    d = '%.2f' % (s % 1)
    return time.strftime(r'%H:%M:%S', time.gmtime(s)) + d.lstrip('0')

@click.command(help='Get duration of media files')
@click.argument('directory', type=click.Path(exists=True), default='.')
def duration(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(f)]
    output = []
    total_duration = 0.0
    total_size = 0
    for f in files:
        length = media_length(f)
        if length is None: continue
        size = os.stat(f).st_size
        output.append([
            click.format_filename(f),
            length[0],
            sizeof_fmt(size),
            size/length[1]/1000*8 if length[1] > 0 else 0
        ])
        total_duration += length[1]
        total_size += size
    
    click.echo("filename,duration,size,bitrate")
    for line in output:
        click.echo('%s,%s,%s,%.1f kbps' % (escape_csv(line[0]), line[1], line[2], line[3]))
    click.echo('-- total --,%s,%s,%.1f kbps' % (
        format_seconds(total_duration),
        sizeof_fmt(total_size),
        total_size/total_duration/1000*8 if total_duration > 0 else 0
    ))


if __name__ == '__main__':
    duration()
