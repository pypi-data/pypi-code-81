class Inventory:
	def __init__(self,stockno,stockname,amount,price):
		self.__stockno = stockno
		self.__stockname = stockname
		self.__amount = amount
		self.__price = price

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
	def price(self):
		return self.__price

	def __str__(self):
		return """
			{
				stockno:%s,
				stockname:%s,
				amount:%s,
				price:%s
			}
		""" % (self.__stockno,self.__stockname,self.__amount,self.__price)

	def toDict(self):
		return {
			"stockno":self.__stockno,
			"stockname":self.__stockname,
			"amount":self.__amount,
			"price":self.__price,
		}