class Tick:
	def __init__(self,stockid,stockname,date \
				,openprice,closeprice,lowprice, \
				highprice,volume):
		self.__stockid = [i for i in set(stockid)][0]
		self.__stockname = [i for i in set(stockname)][0]
		self.__date = date
		self.__openprice = openprice
		self.__closeprice = closeprice
		self.__lowprice = lowprice
		self.__highprice = highprice
		self.__volume = volume

	@property
	def stockid(self):
		return self.__stockid
	@property
	def stockname(self):
		return self.__stockname
	
	@property
	def date(self):
		return self.__date

	@property
	def openprice(self):
		return self.__openprice

	@property
	def closeprice(self):
		return self.__closeprice

	@property
	def lowprice(self):
		return self.__lowprice

	@property
	def highprice(self):
		return self.__highprice

	@property
	def volume(self):
		return self.__volume

	def __str__(self):
		return """
			{
				"stockid":%s,
				"stockname":%s,
				"date":%s,
				"openprice":%s,
				"closeprice":%s,
				"lowprice":%s,
				"highprice":%s,
				"volume":%s,
			}
		""" %(self.__stockid,self.__stockname,self.__date,self.__openprice, \
			self.__closeprice,self.__lowprice,self.__highprice, \
			self.__volume)
	
	def toDict(self):
		return {
				"date":self.__date,
				"openprice":self.__openprice,
				"closeprice":self.__closeprice,
				"lowprice":self.__lowprice,
				"highprice":self.__highprice,
				"volume":self.__volume,
		}


