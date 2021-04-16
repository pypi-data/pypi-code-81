import asyncio
import datetime
import os
import time
from autosync import model
from autosync import lib
from autosync import utils
from tabulate import tabulate
import pandas as pd
from dateutil import tz
from click import echo

async def RUN(configFile="testing/config.json"):
    start_time = time.perf_counter()
    echo(f'Start time: {start_time:0.5f}')
    mnets = {}
    masternet = {}
    cfg = model.APPCONFIG(configFile)
    mpi = lib.MerakiApi(cfg)
    db = mpi.getAPI()
    echo("LOADING CONFIG FROM ENV")
    masterOrg = model.ORGDB(cfg.tag_master, cfg.tag_target)
    masternet.update({'master': masterOrg})
    masternet['master'].networks.update({'master': 'Master'})
    if cfg.USE_CACHE:
        lib.loadCache(masterOrg, cfg)
    if cfg.ALL_ORGS:
        await utils.getOrginizationsAll(db, mnets)
    else:
        orgList = cfg.whitelist
        orgdbTasks = [
            utils.getOrginizationsWhiteList(db, org, mnets) for org in orgList
        ]
        await asyncio.gather(*orgdbTasks)

    orgThreads = []
    validateThread = []
    for org in mnets:
        orgThreads.append(
            utils.OrgSyncProcessor(mnets[org], cfg, masternet['master'], db))
    [orgThread.start() for orgThread in orgThreads]
    [orgThread.join() for orgThread in orgThreads]
    for org in mnets:
        validateThread.append(
            utils.ValidateOrginization(mnets[org], cfg, masternet['master']))
    [thread.start() for thread in validateThread]
    [thread.join() for thread in validateThread]

    if cfg.USE_CACHE:
        masterOrg.lastsync = datetime.datetime.utcnow()
        lib.storeCache(masterOrg, cfg)
    #heckTasks = [mnetutils]

# await utils.batchSync(mnets,masternet,cfg,stdb,db)
    elapsed_time = time.perf_counter() - start_time
    echo(f'Total Job Runtime: {elapsed_time:0.5f} secounds')
    orgcount = 0
    networkCount = 0
    t = []
    tz_local = tz.tzlocal()
    for org in mnets:
        orgcount = orgcount + 1
        networkCount = networkCount + int(len(mnets[org].networks))
        t.append({
            'Orginization Name': mnets[org].name,
            'Total Network': len(mnets[org].networks),
            'Sync Runtime': mnets[org].syncruntime,
            'Last Sync': mnets[org].lastsync
        })
    echo(
        f'Total Orgs Synced: {orgcount} Total Network Synced: {networkCount}')
    table = pd.DataFrame.from_dict(t)
    echo(tabulate(table, headers='keys', tablefmt='psql'))

if __name__ == '__main__':
    asyncio.run(RUN())
    echo('Done')


