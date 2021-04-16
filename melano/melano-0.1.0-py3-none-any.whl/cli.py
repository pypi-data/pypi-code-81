import json

import click
from rich.table import Table
from rich.console import Console

from melano.diff import compare


def read_file(path):

    with open(path, 'r') as fp:
        return json.load(fp)


def format_value(value):

    if not value:
        return 'null'

    if isinstance(value, (int, float)):
        return str(value)

    if isinstance(value, bool):
        return 'true' if value else 'false'

    if isinstance(value, dict):
        return json.dumps(value)

    return value


@click.group()
def melano():
    pass


@melano.command()
@click.argument('file1')
@click.argument('file2')
@click.option('--assert-only/--no-assert-only', default=False)
def diff(file1, file2, assert_only):

    diffs = compare(read_file(file1), read_file(file2), assert_only)

    console = Console()
    table = Table(title="Differences", show_lines=True)

    table.add_column('s.no.', justify="center")
    # table.add_column("type", justify="center")
    table.add_column("field")
    table.add_column(file1)
    table.add_column(file2)
    # table.add_column("Message")

    for idx, diff in enumerate(diffs):
        x = format_value(diff.get('x', '-'))
        y = format_value(diff.get('y', '-'))
        color = 'red' if diff['type'] == 'MISSING' else 'yellow'
        table.add_row(
            str(idx+1),
            # diff['type'],
            diff['field'],
            x,
            y,
            # diff['message'],
            style=color)

    console.print(table)


if __name__ == '__main__':
    melano()
