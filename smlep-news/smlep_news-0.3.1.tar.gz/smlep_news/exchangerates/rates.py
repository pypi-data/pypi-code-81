class Rates:
    def __init__(self, d):
        self.base = d["base"]
        self.date_str = d["date"]
        self.rates = d["rates"]

    def __repr__(self):
        return "Exchange rates at {} with {} base".format(self.date_str, self.base)
