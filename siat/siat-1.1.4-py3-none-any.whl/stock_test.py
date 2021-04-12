# -*- coding: utf-8 -*-


import os; os.chdir("S:/siat")
from siat.stock import *

price = stock_price("GOOG", "2019-7-1", "2019-12-31")
prices = compare_stock(["DAI.DE","BMW.DE"], "Close", "2020-1-1", "2020-3-31")
info=candlestick_demo("005930.KS", "2020-1-13", "2020-1-17")
info=candlestick("TCS.NS", "2020-3-1", "2020-3-31")
info=candlestick("0700.HK","2020-2-1","2020-3-31",mav=2,volume=True,style='blueskies')

compare_stock(["FB", "TWTR"], "Daily Ret%", "2020-3-1", "2020-3-31")

compare_stock("UBSG.SW", ["Daily Ret", "log(Daily Ret)"], "2020-1-1", "2020-1-10")
compare_stock("CDI.PA", ["Daily Ret", "log(Daily Ret)"], "2020-1-1", "2020-3-31")

compare_stock("IBM", ["Annual Ret%", "Daily Ret%"], "2019-1-1", "2019-12-31")
compare_stock(["000002.SZ", "600266.SS"], "Annual Ret%", "2020-1-1", "2020-3-31")
compare_stock(["BABA", "JD"], "Annual Ret%", "2020-1-1", "2020-3-31")
compare_stock(["0700.HK", "1810.HK"], "Annual Ret%", "2019-10-1", "2019-12-31")
compare_stock(["MSFT", "AAPL"], "Annual Ret%", "2019-1-1", "2020-3-31")

info=stock_ret("MSFT", "2010-1-1", "2020-12-31", type="Exp Ret%")

compare_stock(["JD", "AMZN"], "Exp Adj Ret%", "2019-1-1", "2020-12-31")


pv=stock_price_volatility("000002.SZ", "2019-1-1", "2020-12-31", "Weekly Price Volatility")
pv=stock_price_volatility("000002.SZ", "2019-1-1", "2020-12-31", "Annual Price Volatility")

compare_stock(["JD", "BABA"], "Annual Price Volatility", "2019-1-1", "2019-12-31")

compare_stock(["JD", "BABA"], "Exp Price Volatility", "2019-1-1", "2019-12-31")

info=stock_ret_volatility("AAPL", "2019-1-1", "2019-12-31", "Weekly Ret Volatility%")
info=stock_ret_volatility("AAPL", "2019-1-1", "2019-12-31", "Annual Ret Volatility%")
info=stock_ret_volatility("AAPL", "2019-1-1", "2019-12-31", "Exp Ret Volatility%")

compare_stock(["AAPL", "MSFT"], "Annual Ret Volatility%", "2019-1-1", "2019-12-31")
compare_stock(["AAPL", "MSFT"], "Exp Ret Volatility%", "2019-1-1", "2019-12-31")

compare_stock("QCOM", ["Annual Ret LPSD%", "Annual Ret Volatility%"], "2019-1-1", "2019-12-31")
compare_stock("QCOM", ["Exp Ret LPSD%", "Exp Ret Volatility%"], "2019-1-1", "2019-12-31")
compare_stock("QCOM", ["Exp Ret LPSD%", "Exp Ret%"], "2019-1-1", "2019-12-31")

compare_stock(["FB", "MSFT"], "Annual Ret LPSD%", "2019-1-1", "2019-12-31")


#==============================================================================
dfr=stock_ret('AAPL','2020-1-1','2021-4-8',type="Daily Adj Ret%")


compare_stock(["000002.SZ", "600266.SS"], "Annual Ret%", "2020-1-1", "2020-3-31")
compare_stock(["BABA", "JD"], "Annual Ret%", "2020-1-1", "2020-3-31")
compare_stock(["0700.HK", "1810.HK"], "Annual Ret%", "2020-1-1", "2020-3-31")
compare_stock(["MSFT", "AAPL"], "Annual Ret%", "2019-1-1", "2020-3-31")

info=stock_ret("MSFT", "2010-1-1", "2020-3-31", type="Exp Ret%")




#==============================================================================
vix=security_price("^VIX", "2020-1-1", "2021-3-31",power=15)
vix=security_price("^VIX", "2021-1-1", "2021-3-31",power=10)

compare_security(['^VIX','^GSPC'],'Close','2011-1-1','2020-12-31',twinx=True)


compare_stock("AAPL", ["Close", "Adj Close"], "2019-1-1", "2019-12-31")
compare_stock("000002.SZ", ["Close", "Adj Close"], "2019-1-1", "2019-7-31")



pricedf=get_price('^HSI',"1991-1-1","2021-2-28")


df=security_price('AAPL','2021-1-1','2021-1-31',datatag=True,power=4)

info=get_stock_profile("AAPL")
info=get_stock_profile("MSFT",info_type='officers')
info=get_stock_profile("AAPL",info_type='officers')
info=stock_info('AAPL')
sub_info=stock_officers(info)

div=stock_dividend('600519.SS','2011-1-1','2020-12-31')
split=stock_split('600519.SS','2000-1-1','2020-12-31')

ticker='AAPL'
info=stock_info(ticker)
info=get_stock_profile("AAPL",info_type='officers')

info=get_stock_profile("AAPL")

info=get_stock_profile("MSFT",info_type='officers')
info=get_stock_profile("GS",info_type='officers')

info=stock_info('JD')
sub_info=stock_officers(info)
info=get_stock_profile("JD",info_type='officers')

info=stock_info('BABA')
sub_info=stock_officers(info)
info=get_stock_profile("BABA",info_type='officers')

info=stock_info('0700.HK')
sub_info=stock_officers(info)
info=get_stock_profile("0700.HK",info_type='officers')

info=stock_info('600519.SS')
sub_info=stock_officers(info)
info=get_stock_profile("600519.SS",info_type='officers')

info=get_stock_profile("0939.HK",info_type='risk_esg')


market={'Market':('China','^HSI')}
stocks={'0700.HK':3,'9618.HK':2,'9988.HK':1}
portfolio=dict(market,**stocks)
esg=portfolio_esg2(portfolio)



