#!/usr/bin/python3
import click
import os
import shutil
from os.path import basename, splitext

def splitpath(path):
    segments = os.path.normpath(path).split(os.path.sep)
    if segments: segments[0] += os.sep
    return segments

def up(path, level=1):
    segments = splitpath(path)
    return os.path.join(*segments[:-level])

def dircontent(path, _type=None):
    content = [os.path.join(path, f) for f in os.listdir(path)]
    if _type == 'f': content = [a for a in content if os.path.isfile(a)]
    return content

def up_with_prefix(path, prefix):
    base = basename(path)
    return os.path.join(up(path, 2), prefix+base)

@click.command(help='Move content of a directory up while combining the filename with dirname')
@click.argument('directories', type=click.Path(exists=True), nargs=-1)
@click.option('--sep', '-s', default='.', help='separator for joining directory names')
@click.option('--namefromlargest', '-b', is_flag=True, help='Get name prefix from biggest file in parent directory')
@click.option('--yes', '-y', is_flag=True, help='Do not ask for confirmation')
def moveup(directories, sep, namefromlargest, yes):
    for directory in directories:
        directory = os.path.abspath(directory)
        if not os.path.isdir(directory):
            click.secho("'%s' is not a directory" % directory, fg='red', err=True)
            continue
        parent = up(directory)
        content = [os.path.join(directory, f) for f in os.listdir(directory)]
        if not content:
            click.secho("'%s' is empty" % directory, fg='red', err=True)
            continue

        prefix = basename(directory)
        if namefromlargest:
            largest = sorted(dircontent(parent, 'f'), key=os.path.getsize, reverse=True)[:1]
            if not largest:
                click.secho("'%s' contains no files: cannot find largest" % parent , fg='red', err=True)
                continue
            prefix, _ = splitext(basename(largest[0]))
        prefix += sep

        job = [(p, up_with_prefix(p, prefix)) for p in content]
        for src, dst in job:
            click.secho(src, fg='yellow', nl=False)
            click.echo(' -> ')
            click.secho(dst, fg='green')
            click.echo()
        
        if yes or click.confirm('do you want to continue'):
            for src, dst in job:
                shutil.move(src, dst)
            if not dircontent(directory):
                os.rmdir(directory)
            click.secho('done.', bold=True)

if __name__ == '__main__':
    moveup()