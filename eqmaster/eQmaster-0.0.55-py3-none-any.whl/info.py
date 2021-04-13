import pandas

def get_listed_companies():
    
    stock_general_df = pandas.read_csv('s3://ephod-tech.trading-advisor.auto-trade.tw.data.validated/EWNPRCSTD/stock_attributes.csv')
    listed_companies = stock_general_df.loc[(stock_general_df['delist_date'].isna())&(stock_general_df['stype']=='STOCK')&(stock_general_df['market']=='TSE')]
    return listed_companies

def get_indices():
    stock_general_df = pandas.read_csv('s3://ephod-tech.trading-advisor.auto-trade.tw.data.validated/EWIPRCSTD/indx_attributes.csv')
    listed_indices = stock_general_df.loc[(stock_general_df['delist_date'].isna())&(stock_general_df['market']=='TSE')]
    return listed_indices

    