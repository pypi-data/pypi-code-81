from enum import Enum


"""
tradeType : 交易類型
分為 整股、盤後、零股
"""
tradeType_Common = "Common" # 整股
# tradeType_AMT = "AMT" # 盤後
tradeType_Odd = "Odd" # 盤後零股
tradeType_Fixing = "Fixing" # 盤後定價交易(定盤)
tradeType_IntradayOdd = "IntradayOdd" # 盤中零股

"""
tradeCategory : 交易種類
分為現股、融資、融券
"""
tradeCategory_Cash = "Cash" # 現股
tradeCategory_Margin = "marginTrading" # 融資
tradeCategory_Short = "ShortSelling" # 融券

"""
pendingType: 掛單種類
分為ROC、IOC、FOK
"""
pendingType_ROC = "ROD"
pendingType_IOC = "IOC"
pendingType_FOK = "FOK"

"""
orderType : 買賣
"""
orderType_Buy = "Buy"
orderType_Sell = "Sell"

"""
takePrice: 取價類型
分為跌停、漲停、現價
"""
takePrice_LimitDown = "LimitDown" # 跌停
takePrice_LimitUp = "LimitUp" # 漲停
takePrice_Unchanged = "Unchanged" # 現價

class StockEnum(str,Enum):
	Common = tradeType_Common
	# AMT = tradeType_AMT
	# Odd = tradeType_Odd
	Odd = tradeType_Odd
	Fixing = tradeType_Fixing
	IntradayOdd = tradeType_IntradayOdd
	Cash = tradeCategory_Cash
	MarginTrading = tradeCategory_Margin
	ShortSelling = tradeCategory_Short
	ROD = pendingType_ROC
	IOC = pendingType_IOC
	FOK = pendingType_FOK
	Buy = orderType_Buy
	Sell = orderType_Sell
	LimitDown = takePrice_LimitDown
	LimitUp = takePrice_LimitUp
	Unchanged = takePrice_Unchanged