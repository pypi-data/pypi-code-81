import click
import os, sys, re

def partition(pred, arr):
    t, f = [], []
    for e in arr:
        (t if pred(e) else f).append(e)
    return t, f

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]    

@click.command(help='Rename files/directories inside a text editor')
@click.argument('path', default='.')
def rename(path):
    if not os.path.isdir(path):
        click.echo('%s is not a directory' % path, err=True)
        sys.exit()
    files = os.listdir(path)
    files.sort(key=natural_sort_key)
    dirs, files = partition(os.path.isdir, files)

    original = '\n'.join(files)
    renamed = click.edit(original)
    if renamed: renamed = renamed.strip()

    if (not renamed or renamed == original):
        click.echo('nothing''s changed')
        sys.exit()

    renamed = renamed.split('\n')

    if (len(renamed) != len(files)):
        click.echo('wrong number of rows')
        sys.exit()

    changed = [(a, b) for a, b in zip(files, renamed) if a != b]
    for a, b in changed:
        click.secho(a, bold=True, nl=False)
        click.echo(' -> ', nl=False)
        click.secho(b, bold=True, nl=True)

    confirmed = click.confirm('Do you want to continue?', abort=True)

    if confirmed:
        for a, b in changed:
            os.rename(a, b)
        click.secho('Files has been renamed!', fg='green', bold=True)
