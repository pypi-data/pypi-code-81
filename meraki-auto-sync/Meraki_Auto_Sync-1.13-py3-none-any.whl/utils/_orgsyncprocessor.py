import threading
import time
from autosync import lib
from autosync import model
import asyncio
import logging
from datetime import datetime
from .processor import proccessNetwork
from click import print
class OrgSyncProcessor(threading.Thread):
    def __init__(self,org,appcfg,masternet,api):
        threading.Thread.__init__(self)
        self.org = org
        self.appcfg=appcfg
        self.masternet = masternet
        self.api = api
        
    def run(self):
        start_time = time.perf_counter()
        threading.currentThread().setName(self.org.name)
        if self.appcfg.DEBUG:
            print(f'\tOrgName: {self.org.name} Sync Started at: {start_time} '
              f'Thread PID:{threading.currentThread().native_id}')
     
        nets = asyncio.run(self._getOrgNetworks())

        if self.appcfg.USE_CACHE:
            lib.loadCache(self.org, self.appcfg)
            self.org.name
        if not self.org.cached:
            for net in nets:
                if self.appcfg.tag_master in net['tags'] or net['id'] == 'L_575334852396597314':
                   self.masternet.networks['master'] = model.MNET(net)
                self.org.networks.update({net['id']:model.MNET(net)})
                #net_start_time = time.perf_counter()
                
                #self.org.networks[net['id']].syncruntime = \
                #    time.perf_counter() - net_start_time
            asyncio.run(self._asyncRun())
            self.org.syncruntime = time.perf_counter() - start_time
            self.org.lastsync = datetime.utcnow()
            lib.storeCache(self.org, self.appcfg)
        else:
            print(f'OrgName: {self.org.name} Loaded From Cache Date: {self.org.lastsync}')


    async def _asyncRun(self):
        with lib.MerakiAsyncApi(self.appcfg) as db:
            logger = logging.getLogger('meraki.aio')
            logger.setLevel(logging.WARNING)
            netTasks = [proccessNetwork(self.org.networks[net], self.appcfg, self.masternet.networks['master'], db)
                        for net in self.org.networks]
            await asyncio.gather(*netTasks)
    
    async def _getOrgNetworks(self):
        with lib.MerakiAsyncApi(self.appcfg) as db:
            return  await db.organizations.getOrganizationNetworks(self.org.id)