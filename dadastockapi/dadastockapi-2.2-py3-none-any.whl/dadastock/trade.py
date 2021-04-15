class Trade:
	def __init__(self,orderno,stockno,stockname \
		,amount,orderType,price, \
		tradeCategory,tradeType,takeprice,pendingType,state):
		self.__orderno = orderno
		self.__stockno = stockno
		self.__stockname = stockname
		self.__amount = amount
		self.__orderType = orderType
		self.__price = price
		self.__tradeCategory = tradeCategory
		self.__tradeType = tradeType
		self.__takeprice = takeprice
		self.__state = state
		self.__pendingType = pendingType

	@property
	def pendingType(self):
		return self.__pendingType
	@property
	def orderno(self):
		return self.__orderno
	@property
	def stockno(self):
		return self.__stockno
	@property
	def stockname(self):
		return self.__stockname
	@property
	def amount(self):
		return self.__amount
	@property
	def orderType(self):
		return self.__orderType
	@property
	def price(self):
		return self.__price
	@property
	def state(self):
		return self.__state

	@property
	def tradeCategory(self):
		return self.__tradeCategory
	@property
	def tradeType(self):
		return self.__tradeType
	@property
	def takeprice(self):
		return self.__takeprice

	def __str__(self):
		return """
			{
				orderno:%s,
				stockno:%s,
				stockname:%s,
				amount:%s,
				orderType:%s,
				price:%s,
				tradeCategory:%s,
				tradeType:%s,
				takeprice:%s,
				pendingType:%s,
				state:%s,

			}
		""" % (self.__orderno,self.__stockno,self.__stockname, \
			self.__amount,self.__orderType,self.__price, \
			self.__tradeCategory,self.__tradeType,self.__takeprice,self.__pendingType,self.__state)

	def toDict(self):
		return 	{
				"orderno":self.__orderno,
				"stockno":self.__stockno,
				"stockname":self.__stockname,
				"amount":self.__amount,
				"orderType":self.__orderType,
				"price":self.__price,
				"tradeCategory":self.__tradeCategory,
				"tradeType":self.__tradeType,
				"takeprice":self.__takeprice,
				"pendingType":self.__pendingType,
				"state":self.__state,

		}