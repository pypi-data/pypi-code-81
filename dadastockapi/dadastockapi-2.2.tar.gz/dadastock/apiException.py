class secretClientIdException(Exception):
	def __init__(self,message = "secretClientId not found, please login first"):
		self.message = message
		super().__init__(self.message)

class secretTokenException(Exception):
	def __init__(self,message = "secretToken not found, please login first"):
		self.message = message
		super().__init__(self.message)

class InternalServerException(Exception):
	def __init__(self,message = "backend internal Server Error"):
		self.message = message
		super().__init__(self.message)

class LoginException(Exception):
	def __init__(self,status_code,message):
		self.message = """status_code %s,%s""" %(status_code,message)
		super().__init__(self.message)

class TradeException(Exception):
	def __init__(self,status_code,message):
		self.message = """status_code %s,%s""" %(status_code,message)
		super().__init__(self.message)

class TickException(Exception):
	def __init__(self,status_code,message):
		self.message = """status_code %s,%s""" %(status_code,message)
		super().__init__(self.message)

class LackParameterException(Exception):
	def __init__(self,message="lack of parameter"):
		self.message = message
		super().__init__(self.message)

class InventoryException(Exception):
	def __init__(self,status_code,message):
		self.message = message
		super().__init__(self.message)

class OrderParameterException(Exception):
	def __init__(self,status_code,message):
		self.message = """status_code %s,%s""" %(status_code,message)
		super().__init__(self.message)

class BalanceAPIException(Exception):
	def __init__(self,status_code,message):
		self.message = """status_code %s,%s""" %(status_code,message)
		super().__init__(self.message)