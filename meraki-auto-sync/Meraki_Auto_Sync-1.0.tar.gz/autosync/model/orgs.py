class ORGDB (object):
	def __init__(self,orgId,orgName):
		self.db = None
		self.id = orgId
		self.name = orgName
		self.syncruntime = None
		self.lastsync = None
		self.cached = False
		self.networks = {}
	def __dir__(self):
		return self.__dict__.keys()