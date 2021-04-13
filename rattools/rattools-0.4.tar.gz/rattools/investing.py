
def get_stock_data(tickers):
    
    import finviz
    import pandas as pd

    sp500 = pd.DataFrame()
    
    for ticker in tickers:
        try:
            stock = finviz.get_stock(ticker)
    
            df = pd.DataFrame.from_dict(stock, orient='index').T
            df["ticker"] = ticker
            sp500 = sp500.append(df)
        except:
            pass
    return sp500