import datetime
import os
import random
import sys
import time

import numpy as np
import pandas as pd
import streamlit as st
from tqdm import tqdm, trange

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from .GetData import HolidayStockData, StockData
except:
    from GetData import HolidayStockData, StockData


st.title('Suluoya Stock')


def get_stock_data():
    global StockData
    stock_list = st.text_area('stock', '隆基股份\n贵州茅台')
    stock_list = stock_list.split('\n')
    start_date = str(st.date_input(
        'start date',
        datetime.date(2019, 11, 1)))
    end_date = str(st.date_input(
        'end date',
        datetime.date(2020, 12, 31)))
    frequency = st.selectbox('frequency', ['d', 'w', 'm'])
    StockData = StockData(names=stock_list,
                          start_date=start_date,
                          end_date=end_date,
                          frequency=frequency)
    stock_pair, stock_data = StockData.stock_data[1:]
    StockData.quit()
    for i, j in stock_pair.items():
        i, ":", j
    stock_data
    data = []
    for date in stock_data['date']:
        close = stock_data[stock_data['date'] == date]['close']
        data.append(list(close))
    st.line_chart(pd.DataFrame(data, columns=stock_list))


get_stock_data()
