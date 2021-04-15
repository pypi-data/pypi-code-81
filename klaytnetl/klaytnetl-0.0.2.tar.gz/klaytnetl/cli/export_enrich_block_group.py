# MIT License
#
# Copyright (c) 2021 Jetson, jetson@contxts.io
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
import tempfile, shutil

from blockchainetl.logging_utils import logging_basic_config
from klaytnetl.jobs.export_enrich_block_group_job import ExportEnrichBlockGroupJob
from klaytnetl.jobs.exporters.enrich_block_group_item_exporter import enrich_block_group_item_exporter
from klaytnetl.providers.auto import get_provider_from_uri, get_kas_provider_from_uri
from klaytnetl.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-b', '--batch-size', default=100, type=int, help='The number of blocks to export at a time.')
@click.option('-p', '--provider-uri', type=str, help='Klaytn Node IP address & port, http://localhost:8551')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--blocks-output', default=None, type=str,
              help='The output file for blocks. If not provided blocks will not be exported. Use "-" for stdout')
@click.option('--transactions-output', default=None, type=str,
              help='The output file for transactions. '
                   'If not provided transactions will not be exported. Use "-" for stdout')
@click.option('--logs-output', default=None, type=str,
              help='The output file for logs. If not provided logs will not be exported. Use "-" for stdout')
@click.option('--token-transfers-output', default=None, type=str,
              help='The output file for token transfers. '
                   'If not provided token transfers will not be exported. Use "-" for stdout')
@click.option('--file-format', default='json', type=str,
              help='Export file format. "json" (default) or "csv".')
@click.option('--file-maxlines', default=None, type=int,
              help='Limit max lines per single file. '
                   'If not provided, output will be a single file.')
@click.option('--compress', is_flag=True, type=bool, default=False,
              help='Enable compress option using gzip. '
                   'If not provided, the option will be disabled.')
@click.option('--api-service', default='web3', type=str,
              help='')
@click.option('--auth-id', default=None, type=str,
              help='')
@click.option('--auth-secret', default=None, type=str,
              help='')
@click.option('--x-chain-id', default="8217", type=str,
              help='')
def export_enrich_block_group(start_block, end_block, batch_size, provider_uri, max_workers,
                              blocks_output, transactions_output, logs_output, token_transfers_output,
                              file_format='json', file_maxlines=None, compress=False, api_service='web3', auth_id=None, auth_secret=None, x_chain_id="8217"):
    """Exports block groups from Klaytn node."""

    if blocks_output is None and transactions_output is None and logs_output is None and token_transfers_output is None:
        raise ValueError('At least one of --blocks-output, --transactions-output, --logs-output, or --token-transfers-output options must be provided')

    if file_format not in {'json', 'csv'}:
        raise ValueError('"--file-format" option only supports "json" or "csv".')

    if isinstance(file_maxlines, int) and file_maxlines <= 0:
        file_maxlines = None

    exporter_options = {
        'file_format': file_format,
        'file_maxlines': file_maxlines,
        'compress': compress
    }

    if api_service == 'kas':
        headers = {
            "ContentType": "application/json",
            "x-chain-id": "8217"
        }
        if x_chain_id is not None and isinstance(x_chain_id, str):
            headers['x-chain-id'] = x_chain_id

        web3_provider = ThreadLocalProxy(lambda: get_kas_provider_from_uri(
            provider_uri,
            auth=(auth_id, auth_secret),
            headers=headers))
    else:
        web3_provider = ThreadLocalProxy(lambda: get_provider_from_uri(provider_uri, batch=True))


    job = ExportEnrichBlockGroupJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=1 if api_service == 'kas' else batch_size,
        batch=False if api_service == 'kas' else True,
        batch_web3_provider=web3_provider,
        max_workers=max_workers,
        item_exporter=enrich_block_group_item_exporter(blocks_output,
                                                       transactions_output,
                                                       logs_output,
                                                       token_transfers_output,
                                                       **exporter_options),
        export_blocks=blocks_output is not None,
        export_transactions=transactions_output is not None,
        export_logs=logs_output is not None,
        export_token_transfers=token_transfers_output is not None)
    job.run()
