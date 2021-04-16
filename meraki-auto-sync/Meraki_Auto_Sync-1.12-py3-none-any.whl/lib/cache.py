from datetime import datetime
import pickle
from os import path, remove
from click import echo
def cacheAge(self):
	return datetime.utcnow() - self.last_sync


# returns the cached object if exists otherwise returns the locally synced
def loadCache(org,appcfg):
	f = f'{appcfg.CACHE_DIR}/{str(org.id)}-{str(org.name)}.mnet'
	if path.exists(f) and appcfg.USE_CACHE:
		with open (f, "rb") as pFile:
			org_cached = pickle.load(pFile)
		if org_cached.lastsync is None:
			echo(f'Has Cache! But it is stale, re-syncing')
			clearCache(org,appcfg)
			org.cached = False

		elif (datetime.utcnow() - org_cached.lastsync) < appcfg.checkCache():
			org.__dict__ = org_cached.__dict__.copy()

		else:
			print(f'Cache File Error! But it is stale, re-syncing')
			clearCache(appcfg)
			org.cached = False

	else:
		echo('No Cahce Found')
		org.cached = False

		
		
# writes it to disk for faster load times
def storeCache(org,appcfg):
	if not appcfg.USE_CACHE: return
	org.cached = True
	f = f'{appcfg.CACHE_DIR}/{str(org.id)}-{str(org.name)}.mnet'
	pickle.dump(org, open(f, "wb"))


# clears cache and kills disk backup
def clearCache(org,appcfg):
	f = f'{appcfg.CACHE_DIR}{str(org.id)}-{str(org.name)} .mnet'
	if path.exists(f):
		remove(f)

# master SYNC function
