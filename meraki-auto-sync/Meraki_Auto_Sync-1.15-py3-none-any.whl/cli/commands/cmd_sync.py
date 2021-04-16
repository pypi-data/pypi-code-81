import asyncio
import os
import click
from autosync import RUN


@click.group()
def cli():
    """ Tasks to start sync auto Sycn of Meraki Networks """
    pass


@click.command(help='Starts Meraki Dashboard Autosyn')
@click.option('-a', '--allOrgs')
@click.option('-c', '--useCache')
@click.option('-d','--debug')
@click.option('-f','--configfile')
@click.option('-k', '--merakiApiKey')
@click.option('-m', '--masterTag')
@click.option('-o', '--autoSyncOrgs')
@click.option('-s', '--suppressLogging')
@click.option('-t', '--targetTag')
@click.option('-T', '--cacheTimeOut')
@click.option('-w', '--write')
@click.option('--tagOverRide')
def start(suppresslogging=None, merakiapikey=None, write=None, allorgs=None, autosyncorgs=None,
          usecache=None, cachetimeout=None, mastertag=None, targettag=None, tagoverride=None,
          logginglevel=None,configfile=None,debug=None):
    if not configfile is None:
        asyncio.run(RUN(configfile))
    else:
        cfg ={}
        cfg['suppress_logging'] = suppresslogging
        cfg['MERAKI_DASHBOARD_API_KEY'] = merakiapikey
        cfg['WRITE'] = write
        cfg['whitelist'] = autosyncorgs
        cfg['tag_master'] = mastertag
        cfg['tag_target'] = targettag
        cfg['ALL_ORGS'] = allorgs
        cfg['USE_CACHE'] = usecache
        cfg['CACHE_TIMEOUT'] = cachetimeout
        cfg['tag_override'] = tagoverride
        cfg['LOGGING_LEVEL'] = logginglevel
        cfg['DEBUG'] = debug
        asyncio.run(RUN(cfg))




cli.add_command(start)
