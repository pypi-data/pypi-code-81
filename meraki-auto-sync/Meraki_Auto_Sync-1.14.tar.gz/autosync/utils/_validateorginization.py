import threading
from autosync import lib
import asyncio
import logging
from .processor import validateNetworkProcessor
 
class ValidateOrginization(threading.Thread):
	def __init__(self,org,appcfg,masternet):
		threading.Thread.__init__(self)
		self.org = org
		self.appcfg=appcfg
		self.oFunctions = None
		self.masternet = masternet
	def run(self):
		asyncio.run(self._asyncRun())
		lib.storeCache(self.org, self.appcfg)

	async def _asyncRun(self):
		print(f'\tOrgName: {self.org.name}Thread PID:{threading.currentThread().native_id}')
		threading.currentThread().setName(self.org.name)
		print(f'\tThread Name:{threading.currentThread().name}')
		with lib.MerakiAsyncApi(self.appcfg) as db:
			logger = logging.getLogger('meraki.aio')
			logger.setLevel(logging.WARNING)
			netCompareTask = [
					validateNetworkProcessor(self.org.networks[net], self.appcfg, self.masternet.networks['master'],db,self.oFunctions) for
					net in self.org.networks if self.appcfg.tag_master not in self.org.networks[net].tags]

			await asyncio.gather(*netCompareTask)