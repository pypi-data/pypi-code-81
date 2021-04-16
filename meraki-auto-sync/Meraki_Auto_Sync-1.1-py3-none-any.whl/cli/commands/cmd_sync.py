import asyncio
import os
import click
from autosync import RUN


@click.group()
def cli():
    """ Tasks to start sync auto Sycn of Meraki Networks """
    pass


@click.command(help='Starts Meraki Dashboard Autosyn')
@click.option('-s', '--suppressLogging', default=lambda: os.environ.get('suppress_logging', 'True'),
              show_default=os.environ.get('suppress_logging', 'True'))
@click.option('-k', '--merakiApiKey', default=lambda: os.environ.get('MERAKI_DASHBOARD_API_KEY'),
              show_default=os.environ.get('MERAKI_DASHBOARD_API_KEY', '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'))
@click.option('-w', '--write', default=lambda: os.environ.get('AUTOSYNC_WRITE', 'False'),
              show_default=os.environ.get('AUTOSYNC_WRITE', 'True'))
@click.option('-a', '--allOrgs', default=lambda: os.environ.get('AUTOSYNC_ALL_ORGS', 'True'),
              show_default=os.environ.get('AUTOSYNC_ALL_ORGS', 'False'))
@click.option('-o', '--autoSyncOrgs', default=lambda: os.environ.get('AUTOSYNC_ORGS', 'None'),
              show_default=os.environ.get('AUTOSYNC_ORGS', 'None'))
@click.option('-c', '--useCache', default=lambda: os.environ.get('USE_CACHE', 'True'),
              show_default=os.environ.get('USE_CACHE', 'True'))
@click.option('-t', '--cacheTimeOut', default=lambda: os.environ.get('CACHE_TIMEOUT', '24'),
              show_default=os.environ.get('CACHE_TIMEOUT', '24'))
@click.option('-m', '--masterTag', default=lambda: os.environ.get('TAG_MASTER', 'master'),
              show_default=os.environ.get('TAG_MASTER'))
@click.option('-t', '--targetTag', default=lambda: os.environ.get('TAG_TARGET', 'autoSYNC'),
              show_default=os.environ.get('TAG_TARGET', 'autoSYNC'))
@click.option('--tagOverRide', default=lambda: os.environ.get('TAG_OVERRIDE', 'False'),
              show_default=os.environ.get('TAG_OVERRIDE', 'False'))
@click.option('-l', '--loggingLevel', default=lambda: os.environ.get('LOGGING_LEVEL', 'ERROR'),
              show_default=os.environ.get('LOGGING_LEVEL', 'ERROR'))
def start(suppresslogging, merakiapikey, write, allorgs, autosyncorgs,
          usecache, cachetimeout, mastertag, targettag, tagoverride,
          logginglevel):
    os.environ['suppress_logging'] = suppresslogging
    os.environ['MERAKI_DASHBOARD_API_KEY'] = merakiapikey
    os.environ['AUTOSYNC_WRITE'] = write
    os.environ['AUTOSYNC_ORGS'] = autosyncorgs
    os.environ['TAG_MASTER'] = mastertag
    os.environ['TAG_TARGET'] = targettag
    os.environ['AUTOSYNC_ALL_ORGS'] = allorgs
    os.environ['USE_CACHE'] = usecache
    os.environ['CACHE_TIMEOUT'] = cachetimeout
    os.environ['TAG_OVERRIDE'] = tagoverride

    asyncio.run(RUN())


cli.add_command(start)
