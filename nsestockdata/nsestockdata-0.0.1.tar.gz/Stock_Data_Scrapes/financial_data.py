from bs4 import BeautifulSoup
import requests as rq 
import pandas as pd

def T_M_B_converter(elemment):
    if "T" in elemment:
        elemment = elemment.replace("T","")
        elemment = elemment.replace(",","")
        elemment = float(elemment) * 1000000000000
    else:
        if "B" in elemment:
            elemment = elemment.replace("B","")
            elemment = elemment.replace(",","")
            elemment = float(elemment) * 1000000000
        else:
            if "M" in elemment:
                elemment = elemment.replace("M","")
                elemment = elemment.replace(",","")
                elemment = float(elemment) * 1000000
            else:
                print("Error - in value")

    return float(elemment)

def get_market_cap(stock):
    url = f"https://in.finance.yahoo.com/quote/{stock}.NS"
    data = pd.read_html(url)
    market_cap = data[1].at[0,1]
    market_cap = T_M_B_converter(market_cap)

    return float(market_cap)

def get_Earnings_Per_Share(stock):
    url = f"https://in.finance.yahoo.com/quote/{stock}.NS"
    data = pd.read_html(url)
    earnings_per_share = data[1].at[3,1]
    earnings_per_share = earnings_per_share.replace(",","")

    return float(earnings_per_share)

def get_average_stock_volume(stock):
    url = f"https://in.finance.yahoo.com/quote/{stock}.NS"
    data = pd.read_html(url)
    avg_volume = data[0].at[7,1]
    avg_volume = avg_volume.replace(",","")

    return float(avg_volume)

def get_enterprise_value(stock):
    url = f"https://in.finance.yahoo.com/quote/{stock}.NS/key-statistics"
    data = pd.read_html(url)
    enterprice_value = data[0].at[1,1]
    enterprice_value = T_M_B_converter(enterprice_value)

    return float(enterprice_value)

def get_price_to_sales_ratio(stock):
    url = f"https://in.finance.yahoo.com/quote/{stock}.NS/key-statistics"
    data = pd.read_html(url)
    price_to_sales_ratio = data[0].at[5,1]
    price_to_sales_ratio = price_to_sales_ratio.replace(",","")

    return float(price_to_sales_ratio)

def get_price_to_book_ratio(stock):
    url = f"https://in.finance.yahoo.com/quote/{stock}.NS/key-statistics"
    data = pd.read_html(url)
    price_to_book_ratio = data[0].at[6,1]
    price_to_book_ratio = price_to_book_ratio.replace(",","")

    return float(price_to_book_ratio)     


