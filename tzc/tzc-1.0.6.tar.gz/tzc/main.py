#!/usr/bin/env python3

import arrow
import click
import re
import sys

@click.command()
@click.version_option()
@click.option('-i', '--input-zone', default='utc', help='timezone in file')
@click.option('-o', '--output-zone', default='local', envvar='TZ', help='output timezone')
@click.option('-f', '--format', '_format', default=None, help='output format (strptime)')
@click.option('-s', '--short', default=False, is_flag=True, help='format output as YYYY-MM-DD HH:MM:SS')
@click.argument('input-file', type=click.File('r'), default='-')
@click.argument('output-file', type=click.File('w'), default='-')
def cli(input_file, output_file, input_zone, output_zone, _format, short):
    """copy input to output, converting timezone in any lines starting with a timestamp"""
    pattern = re.compile('^(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}\.*\d*[+-]*\d*:*\d*)(.*)$')
    for line in input_file:
        m = pattern.match(line)
        if m:
            time_field, message_field = m.groups()
            timestamp = arrow.get(time_field).to(output_zone)
            if short:
                time_field = timestamp.format(arrow.FORMAT_ATOM)[:19]
            elif _format:
                time_field = timestamp.strftime(_format)
            else:
                time_field = timestamp.isoformat(' ')
            line = f"{time_field}{message_field}\n"
        output_file.write(line)
    return 0
