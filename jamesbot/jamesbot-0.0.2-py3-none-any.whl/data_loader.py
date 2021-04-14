from stock import Stock

class DataLoarder():
    
    def __init__(self, tickers = []):

        self.tickers = []
        self.stocks = {}
        self.add_tickers(tickers)
        
    def load(self, ticker, start_date, end_date):

        if not ticker in self.tickers:

            print('[DATALOADER] Ticker not found: Creating new one ...')
            self.add_tickers([ticker])

        return self.stocks[ticker].load(start_date,end_date)
    
    def add_tickers(self, tickers):

        for ticker in tickers:

            self.tickers.append(ticker)
            stock = Stock(ticker)
            self.stocks[ticker] = stock

        


    



