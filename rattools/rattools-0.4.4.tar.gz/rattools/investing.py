
def get_stock_data(tickers, prices = False, financials = False,
                   info = False, recommendations = False):
    import pandas as pd
    import yfinance as yf
    
    info = {}
    tickers = [ticker.lower() for ticker in tickers]
    
    for ticker in tickers:
    
        try:
            if prices == True:
                stock = yf.Ticker(ticker)
                stock = stock.history(period="max")
                info[ticker] = stock
            
            if financials == True:
                stock = yf.Ticker(ticker)
                stock = stock.financials
                info[ticker] = stock
                
            if info == True:
                stock = yf.Ticker(ticker)
                stock = stock.info
                stock = pd.DataFrame.from_dict(stock, orient = "index").T
                info[ticker] = stock
            
            if recommendations == True:
                stock = yf.Ticker(ticker)
                stock = stock.recommendations
                info[ticker] = stock
                
            
            else:
                pass
        except:
            pass
    return info


