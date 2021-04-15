import os
import warnings
import click

from askanna.core import client

HELP = """
Run Manifest downloader intended to use in askanna-worker
"""

SHORT_HELP = "Download manifest for run"


@click.option(
    "--output", "-o", default="/entrypoint.sh", show_default=True, type=click.Path()
)
@click.command(help=HELP, short_help=SHORT_HELP)
def cli(output):
    warnings.warn("askanna jobrun-manifest is deprecated", DeprecationWarning)
    api_server = client.config.remote
    run_suuid = os.getenv("JOBRUN_SUUID")

    download_url = "/".join(["runinfo", run_suuid, "manifest", ""])
    download_url = api_server + download_url

    r = client.get(download_url)

    with open(output, "w") as f:
        f.write(r.text)
