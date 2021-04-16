import sys
from os import getenv,getcwd,path,mkdir
from distutils.util import strtobool
from datetime import timedelta
from logging import getLevelName
import json

class APPCONFIG:
	def __init__(self,file=None):
		if not file is None:
			self._openConfig(self._getdirectory(file))
		else:
			self._loadFromEnv()
	
	
	def _openConfig(self,file):
		with open(file,'r') as f:
			_config =  json.loads(f.read())
			self._configFromFile(_config)

	def _configFromFile(self,config):
		for item in config:
			setattr(self,item,config[item])
		self.CACHE_DIR = self._getdirectory(self.CACHE_DIR)
		self.log_path = self._getdirectory(self.log_path)
		self.LOGGING_LEVEL = getLevelName(str(self.LOGGING_LEVEL).upper())
		if 'MERAKI_DASHBOARD_API_KEY' not in self.__dict__.keys() or self.MERAKI_DASHBOARD_API_KEY == 'None':
			self.MERAKI_DASHBOARD_API_KEY = getenv('MERAKI_DASHBOARD_API_KEY', None)
			if self.MERAKI_DASHBOARD_API_KEY is None:
				print('Please add MERAKI_DASHBOARD_API_KEY by running "autosync config setkey <API Key>"'
				  	'or add MERAKI_DASHBOARD_API_KEY: <API Key > to your config.json file')
				sys.exit()
		
		
	def _loadFromEnv(self):
		self.USE_ENV = True
		self.MERAKI_DASHBOARD_API_KEY = getenv('MERAKI_DASHBOARD_API_KEY',None)
		if self.MERAKI_DASHBOARD_API_KEY is None:
			print('Please Set MERAKI_DASHBOARD_API_KEY by running autosync config setkey to contunue  or add it to the .env file ')
			sys.exit()
		self.meraki_base_url = getenv('meraki_base_url','https://api.meraki.com/api/v1/')
		self.simulate = bool(strtobool(getenv('simulate','False')))
		self.wait_on_rate_limit = bool(strtobool(getenv('wait_on_rate_limit','True')))
		self.maximum_concurrent_requests = (getenv('maximum_concurrent_requests',3))
		self.nginx_429_retry_wait_time = (getenv('nginx_429_retry_wait_time',8))
		self.maximum_retries = (getenv('maximum_retries',100))
		self.log_path = self._getdirectory(getenv('log_path','~/Logs'))
		self.suppress_logging = bool(strtobool(getenv('suppress_logging', 'False')))
		# Set this to FALSE for READ-ONLY, TRUE for "R/W"
		self.WRITE = bool(strtobool(getenv('WRITE','False')))
		# Set this to true, to crawl all networks. WARNING. Don't set WRITE
		# & ALL_ORGS unless you know what you're doing and dislike your job
		self.ALL_ORGS=bool(strtobool(getenv('ALL_ORGS','False')))
		if self.ALL_ORGS:
			self.whitelist = []
		else:
			## Only monitor these orgs, to keep the "crawl" down
			try:
				self.whitelist = list(getenv('whitelist').split(','))
			except:
				self.whitelist = []
		# Include switch settings?
		self.SWITCH = bool(strtobool(getenv('SWITCH','True')))
		# TARGET should be on ALL networks that are inscope, the master and
		# all the target networks
		self.tag_target = getenv('tag_target','autoSYNC')
		# MASTER should ONLY be on the 'golden network'
		self.tag_master = getenv('tag_master','master')
		#USed for Scale Testing Development
		self.tag_override = bool(strtobool(getenv('tag_override','False')))
		self.OpenRoaming = getenv('OpenRoaming','Meraki123')
		self.CACHE_DIR = self._getdirectory(str(getenv('CHACHE_DIR','~/mnetCache')))
		self.CACHE_TIMEOUT = int(getenv('CACHE_TIMEOUT','24'))
		self.USE_CACHE = bool(strtobool(getenv('USE_CACHE','True')))
		self.CLEAN = bool(strtobool(getenv('CLEAN','True')))
		self.RAD_KEYS_ALL= getenv('RAD_KEYS_ALL','Meraki123')
		try:
			self.SSID_SKIP_PSK=list(getenv('SSID_SKIP_PSK','SSID1,SSID2').split(','))
		except:
			self.SSID_SKIP_PSK = []
		self.LOGGING_LEVEL = getLevelName(str(getenv('LOGGING_LEVEL',"ERROR")).upper())
		self.TARGET_VLAN = bool(strtobool(getenv('TARGET_VLAN','True')))
		self.DEBUG = bool(strtobool(getenv('DEBUG','False')))

	
	def _getdirectory(self,location):
		if str(location).startswith('~/'):
			if not path.exists(path.expanduser(location)):
				mkdir(path.expanduser(location))
			return path.expanduser(location)
		else:
			if not path.exists(path.abspath(location)):
				mkdir(path.abspath(location))
			return path.abspath(location)

	def dumpConfigToFile(self):
		with open('config.json','w+') as f:
			c = self.__dict__
			print(json.dumps(c,indent=4,sort_keys=True))
			f.write(json.dumps(c, indent=4,sort_keys=True))
	
	def getRadSec(self):
		return getenv('RAD_KEYS_ALL')
	def checkCache(self):
		return timedelta(hours=self.CACHE_TIMEOUT)

		