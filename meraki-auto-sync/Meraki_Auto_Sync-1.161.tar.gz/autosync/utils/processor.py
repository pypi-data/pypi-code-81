import asyncio
import datetime
import random
from autosync import mnetutils
import time
import autosync.lib as lib


async def validateNetworkProcessor(networkobj: object,appcfg: object,masternet: object,db: object,oFunc: object):
    """
    ASYNC Function to synclye through configuration dict for network and call the clone functions based on netork id
    Args:

        oFunc:
        networkobj: Current Network Configuration
        masternet: Master Network Configuration
        appcfg: App Configuration Dict based on ENV or Configuration File
        db(object): Meraki SDKI Object
    Returns: Nothing

    """
    print(f'{lib.bc.OKGREEN}Starting Network configuration validation...{lib.bc.ENDC}')
    for product in networkobj.dashboard:

        await mnetutils.clone(networkobj.dashboard[product], masternet.dashboard[product],
                              appcfg, db, networkobj.id, networkobj.name,
                              product, networkobj.functions[product]['update'])

           
           
   



async def proccessNetwork(net: object, appcfg: object, masternet: dict,
                          db):
    """

	Args:
        oFunc:
		net(object): Data Module contains configuration object for the network
		appcfg : App Configuration Dict based on ENV or Configuration File
		masternet: Diect of configuration for master object based on producted
		db (object): Meraki SDKI API Object

	Returns:

	"""
    t1 = time.perf_counter()
    print(f'{lib.bc.OKGREEN}Started Configuration Sync at {t1:0.5f} secound'
          f' for Network: {net.name}')
    approvedList = net.supported
    if appcfg.tag_target in net.tags or appcfg.tag_override:
        if appcfg.tag_master in net.tags or net.id == 'L_575334852396597314':
            await mnetutils.sync(db, net.id, net.name, appcfg,
                                 masternet.dashboard['networks'], 'networks',
                                 masternet.functions['networks']['get'])
        else:
            await mnetutils.sync(db, net.id,net.name, appcfg,
                                 net.dashboard['networks'],'networks',net.functions['networks']['get'])
            
        for product in net.products:
            if product in approvedList:
                waiting = random.randrange(0, 5)
                await asyncio.sleep(waiting)
                if appcfg.tag_master in net.tags or net.id == 'L_575334852396597314':
                    await mnetutils.sync(db, net.id, net.name, appcfg,
                                         masternet.dashboard[product], product,
                                         masternet.functions[product]['get'])
                else:
                    await mnetutils.sync(db, net.id,net.name, appcfg,
                                         net.dashboard[product],product, net.functions[product]['get'])
            else:
                if  appcfg.DEBUG:
                    print(f"No Sync Module for {product}")
                    
        net.lastsync = datetime.datetime.utcnow()
        net.syncruntime = time.perf_counter() - t1
        print(f'{lib.bc.OKGREEN}Built Config From Network: {net.name} '
              f'Process took: {net.syncruntime:0.5f} secounds{lib.bc.Default}')
    
    
    else:
        t = time.perf_counter() - t1
        print(f'Network: {net.name} '
              f'Skiped Syncing Process took: {t:0.5f} secounds')
        
