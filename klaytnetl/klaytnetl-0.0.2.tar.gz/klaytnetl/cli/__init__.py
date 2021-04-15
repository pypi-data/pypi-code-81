# MIT License
#
# Copyright (c) 2021 Jetson, jetson@contxts.io
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import click

from klaytnetl.cli.export_enrich_block_group import export_enrich_block_group
# from klaytnetl.cli.export_raw_block_group import export_raw_block_group
# from klaytnetl.cli.extract_csv_column import extract_csv_column
# from klaytnetl.cli.extract_field import extract_field
# from klaytnetl.cli.filter_items import filter_items
# from klaytnetl.cli.get_block_range_for_date import get_block_range_for_date
from klaytnetl.cli.get_block_range_for_timestamps import get_block_range_for_timestamps
# from klaytnetl.cli.get_keccak_hash import get_keccak_hash
# from klaytnetl.cli.stream import stream


@click.group()
@click.version_option(version='1.6.2')
@click.pass_context
def cli(ctx):
    pass


# export

cli.add_command(export_enrich_block_group, "export_enrich_block_group")
# cli.add_command(export_raw_block_group, "export_raw_block_group")


# streaming
# cli.add_command(stream, "stream")

# utils
# cli.add_command(get_block_range_for_date, "get_block_range_for_date")
cli.add_command(get_block_range_for_timestamps, "get_block_range_for_timestamps")
# cli.add_command(get_keccak_hash, "get_keccak_hash")
# cli.add_command(extract_csv_column, "extract_csv_column")
# cli.add_command(filter_items, "filter_items")
# cli.add_command(extract_field, "extract_field")
