import requests
import json
from stockApi.trade import Trade
from stockApi.tick import Tick
from stockApi.inventory import Inventory
import pandas as pd
from stockApi.stockEnum import StockEnum
from stockApi.apiException import secretClientIdException, \
						secretTokenException, \
						InternalServerException, \
						LoginException, \
						TradeException, \
						OrderParameterException, \
						BalanceAPIException, \
						InventoryException
class stockApi():
	def __init__(self):
		self.secretClientId = ''
		self.secretToken = ''
		self.backendUrl = "http://3.143.234.103:81/"
		self.data = {}
		self.constant = StockEnum
	def login(self,secretClientId,secretToken):
		data = {
			"secretClientId":secretClientId,
			"secretToken":secretToken,
		}
		response = requests.post(self.backendUrl + "api/login/API",json = data)
		try:
			jsondata = json.loads(response.text)
		except Exception as e:
			raise InternalServerException()
		else:
			if jsondata["status"] == 200:
				self.secretClientId = secretClientId
				self.secretToken = secretToken
				self.data = data
				return response.text
			else:
				jsondata = json.loads(response.text)
				raise LoginException(jsondata["status"],jsondata["message"])

	def getBalance(self):
		if not self.secretClientId:
			raise secretClientIdException()
		if not self.secretToken:
			raise secretTokenException()
		data = {
			"secretClientId":self.secretClientId,
			"secretToken":self.secretToken
		}
		response = requests.post(self.backendUrl + "api/user/balanceAPI",json = data)
		try:
			jsondata = json.loads(response.text)
		except Exception as e:
			raise InternalServerException()
		else:
			if jsondata["status"] == 200:
				return jsondata["data"]
			else:
				raise BalanceAPIException(jsondata["status"],jsondata["error"])

	def createOrder(self,stockno,amount, \
		orderType,price,tradeCategory, \
		tradeType,takeprice,pendingType):
		if not self.secretClientId:
			raise secretClientIdException()
		if not self.secretToken:
			raise secretTokenException()
		data = {
			"secretClientId":self.secretClientId,
			"secretToken":self.secretToken,
			"stockno":stockno,
			"amount":amount,
			"orderType":orderType,
			"price":price,
			"tradeCategory":tradeCategory,
			"tradeType":tradeType,
			"takeprice":takeprice,
			"pendingType":pendingType,
		}
		response = requests.post(self.backendUrl + "api/order",json = data)
		try:
			jsondata = json.loads(response.text)
		except Exception as e:
			raise InternalServerException()
		if jsondata["status"] == 200:
			return Trade(**jsondata["data"])
		else:
			if jsondata["status"] == 704 or jsondata["status"] == 703:
				raise OrderParameterException(jsondata["status"],jsondata["error"])
			raise TradeException(jsondata["status"],jsondata["message"]) 
	def checkOrder(self,orderno):
		if not self.secretClientId:
			raise secretClientIdException()
		if not self.secretToken:
			raise secretTokenException()
		data = {
			"secretClientId":self.secretClientId,
			"secretToken":self.secretToken,
			"orderno":orderno
		}
		response = requests.post(self.backendUrl + "api/order",json = data)
		jsondata = json.loads(response.text)
		if jsondata["status"] == 200:
			return Trade(**jsondata["data"])
		else:
			raise TradeException(jsondata["status"],jsondata["message"])
	def cancelOrder(self,trade):
		if not self.secretClientId:
			raise secretClientIdException()
		if not self.secretToken:
			raise secretTokenException()
		orderno = trade.orderno
		data = {
			"secretClientId":self.secretClientId,
			"secretToken":self.secretToken,
			"orderno":orderno
		}
		response = requests.put(self.backendUrl + "api/order",json = data)
		jsondata = json.loads(response.text)
		if jsondata["status"] == 200:
			return Trade(**jsondata["data"])
		else:
			raise TradeException(jsondata["status"],jsondata["message"])

	def modifyOrder(self,trade,modifyType,modifyValue):
		if not self.secretClientId:
			raise secretClientIdException()
		if not self.secretToken:
			raise secretTokenException()
		orderno = trade.orderno
		data = {
			"orderno":orderno,
			"secretClientId":self.secretClientId,
			"secretToken":self.secretToken,
			"modifyType":modifyType,
			"modifyValue":modifyValue
		}
		response = requests.put(self.backendUrl + "api/order",json = data)
		jsondata = json.loads(response.text)
		if jsondata["status"] == 200:
			return Trade(**jsondata["data"])
		else:
			raise TradeException(jsondata["status"],jsondata["message"])

	def stockdata(self,stockno):
		response = requests.post(self.backendUrl + "api/stocks/" + str(stockno))
		jsondata = json.loads(response.text)
		if jsondata["status"] == 200:
			data = jsondata["data"]
			returndata = [[i[j] for i in data] for j in range(8)]
			return Tick(*returndata)
		else:
			raise TickException(jsondata["status"],jsondata["error"])

	def getKBardata(self,stockno,startDate,endDate):
		# datetime format: 20200101
		response = requests.post(self.backendUrl + "api/stocks/{}/{}/{}".format(stockno,startDate,endDate))
		jsondata = json.loads(response.text)
		if jsondata["status"] == 200:
			data = jsondata["data"]
			df = pd.DataFrame(data)
			df.columns = ["stockno","stockname","date","openprice","closeprice","lowprice","highprice","volume"]
			df = df.drop(columns = ["stockno","stockname"])
			df = df.set_index("date")
			return df
		else:
			raise TickException(jsondata["status"],jsondata["error"])

	def getInventory(self):
		if not self.secretClientId:
			raise secretClientIdException()
		if not self.secretToken:
			raise secretTokenException()
		data = {
			"secretClientId":self.secretClientId,
			"secretToken":self.secretToken
		}
		response = requests.post(self.backendUrl + "api/inventory/api",json = data)
		jsondata = json.loads(response.text)
		if jsondata["status"] == 200:
			data = jsondata["data"]
			return [Inventory(**data[i]) for i in range(len(data))]
		else:
			raise InventoryException(jsondata["status"],jsondata["error"])


# api = stockApi()
# loginResult = api.login(
# 	secretClientId = "07f4cce3-8b2d-4793-aa2e-c51bec60c5d2",
# 	secretToken = "437a5b0094323d8e3427385ed09025d832eb36f2a113c549",
# )
# result = api.createOrder(stockno = "1435", \
# 						amount = 1000, \
# 						orderType = api.constant.Buy, \
# 						price = 23.35, \
# 						tradeType = api.constant.Odd, \
# 						tradeCategory = api.constant.Cash, \
# 						takeprice = api.constant.LimitDown, \
# 						pendingType = api.constant.ROD)
# # print(result)

# modifyResult = api.modifyOrder(result,"price",21)

# print(modifyResult)

# check = api.checkOrder(result.orderno)
# r = api.cancelOrder(result)
# print(r)
# print(check)
# print(pd.DataFrame(api.stockdata("1455").toDict()))
# print(api.getKBardata("1435","20210101","20210301"))
# inventories = api.getInventory()
# for inventoryRecord in inventories:
# 	print(inventoryRecord)

# print(api.getBalance())

"""
stockno: 股票代號
tradeType : 交易類型 分為整股(Common)、盤後 (AMT)、零股(Odd)
tradeCategory: 交易種類 分為現股(Cash)、融資(marginTrading)、融券(ShortSelling)
pendingType: 掛單 分為ROD、IOC、FOK
orderType: 買賣類型 分為買(Buy)、賣(Sell)
amount: 數量 int
price: 價格 int
takeprice: 取價 分為跌停(LimitDown)、漲停(LimitUp)、現價(Unchanged)
"""