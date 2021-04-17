from bs4 import BeautifulSoup
import requests as rq 
import pandas as pd

def get_current_price(stock):
    url = f"https://in.finance.yahoo.com/quote/{stock}.NS"
    html = rq.get(url).text    
    soup = BeautifulSoup(html,"lxml")
    price1 = soup.find("div",id="quote-header-info")
    price2 = price1.find("span", class_ ="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
    price3 = price2.text
    price = price3.replace(",","")

    return float(price)

def get_stock_volume(stock):
    url = f"https://in.finance.yahoo.com/quote/{stock}.NS"
    data = pd.read_html(url)
    volume = data[0].at[6,1]
    volume = volume.replace(",","")

    return float(volume)


