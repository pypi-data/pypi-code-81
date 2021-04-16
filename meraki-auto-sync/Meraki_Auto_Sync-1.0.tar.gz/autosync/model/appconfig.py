from os import getenv,getcwd,path
from distutils.util import strtobool
from datetime import timedelta
import json

class APPCONFIG:
	def __init__(self):
		#Meraki SDK Configuration
		self.meraki_api_key = getenv('MERAKI_DASHBOARD_API_KEY','6bec40cf957de430a6f1f2baa056b99a4fac9ea0')
		self.meraki_base_url = getenv('MERAKI_BASE_URL','https://api.meraki.com/api/v1/')
		self.simulate = bool(strtobool(getenv('simulate','False')))
		self.wait_on_rate_limit = bool(strtobool(getenv('wait_on_rate_limit','True')))
		self.maximum_concurrent_requests = (getenv('maximum_concurrent_requests',3))
		self.nginx_429_retry_wait_time = (getenv('nginx_429_retry_wait_time',8))
		self.maximum_retries = (getenv('maximum_retries',100))
		self.log_path = ('log_path','Logs/')
		self.suppress_logging = bool(strtobool(getenv('suppress_logging', 'False')))
		# Set this to FALSE for READ-ONLY, TRUE for "R/W"
		self.WRITE = bool(strtobool(getenv('AUTOSYNC_WRITE','False')))
		# Set this to true, to crawl all networks. WARNING. Don't set WRITE
		# & ALL_ORGS unless you know what you're doing and dislike your job
		self.ALL_ORGS=bool(strtobool(getenv('AUTOSYNC_ALL_ORGS','False')))
		if self.ALL_ORGS:
			self.whitelist = []
		else:
			## Only monitor these orgs, to keep the "crawl" down
			self.whitelist = list(getenv('AUTOSYNC_ORGS').split(','))
		# Include switch settings?
		self.SWITCH = bool(strtobool(getenv('AUTOSYNC_SWITCH','True')))
		# TARGET should be on ALL networks that are inscope, the master and
		# all the target networks
		self.tag_target = getenv('TAG_TARGET','autoSYNC')
		# MASTER should ONLY be on the 'golden network'
		self.tag_master = getenv('TAG_MASTER','msster')
		#USed for Scale Testing Development
		self.tag_override = bool(strtobool(getenv('TAG_OVERRIDE','False')))
		self.OpenRoaming = getenv('RAD_KEYS_OPENROAMING','Meraki123')
		self._ALL_ = getenv('RAD_KEYS_ALL','Meraki123')
		self.CACHE_DIR = path.join(path.expanduser('~'), str(getenv('CHACHE_DIR','mnetCache')))
		self.CACHE_TIMEOUT = int(getenv('CACHE_TIMEOUT','24'))
		self.USE_CACHE = bool(strtobool(getenv('USE_CACHE','True')))
		self.stale_cache = timedelta(hours=self.CACHE_TIMEOUT)
		self.CLEAN = bool(strtobool(getenv('MNET_CLEAN','True')))
		self.RAD_KEYS_ALL= getenv('RAD_KEYS_ALL','Meraki123')
		self.SSID_SKIP_PSK=list(getenv('SSID_SKIP_PSK','SSID1,SSID2').split(','))
		self.TARGET_VLAN = True
		self.DEBUG = False

	def toDICT(self):
		return json.loads(json.dumps(self,default=lambda c: c.__dict__,sort_keys=True))
	def getRadSec(self):
		return getenv('RAD_KEYS_ALL')

		