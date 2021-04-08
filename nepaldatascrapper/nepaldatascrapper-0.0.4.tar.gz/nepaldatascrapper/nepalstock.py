from .scrapper import Scrapper

class NepalStock(Scrapper):
    """
    scraps data from nepalstock.com.np
    """
    def __init__(self):
        endpoints = {
            "todayPrice":
            {
                "endpoint": "/api/nots/nepse-data/today-price",
                "parameter":{"sort":"symbol","size":500,"businessDate":""}, 
            },
            "floorsheet":
            {
                "endpoint": "/api/nots/nepse-data/floorsheet",
                "parameter":{"sort":"contractId,desc","size":1000}
            },
            "security":
            {
                "endpoint": "/api/nots/security",
                "parameter": {}
            },
            "news":
            {
                "endpoint": "/api/nots/news/media/news-and-alerts",
                "parameter": {}
            }
        }
        source = "https://newweb.nepalstock.com.np"
        super().__init__(source, endpoints)

    def getShareInfo(self):
        pass

    def getSharePrices(self,from_date=""):
        """
        get share price
        :param symbol: nepse stock symbol
        :type symbol: str
        :param from_date: get the price of specific date
        :type from_date str

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("todayPrice", businessDate=from_date)
        return self.get("todayPrice", **postData).json()["content"]

    def getSharePrice(self,symbol,from_date=""):
        return [d for d in self.getSharePrices(from_date) if d["symbol"] == symbol]

    def getFloorSheet(self):
        """
        get floor sheet

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("floorsheet")
        data = []
        df = self.get("floorsheet",**postData).json()
        data = df["floorsheets"]["content"]
        total_pages = df["floorsheets"]["totalPages"]
        page = 1
        while page < total_pages:
            postData["page"]=page
            df = self.get("floorsheet",**postData).json()
            data = data + df["floorsheets"]["content"]
            page = page + 1
        return data

    def getSecurities(self):
        """
        get security information

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("security")
        return self.get("security").json()

    def getNews(self):
        """
        get nepse news

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("news")
        return self.get("news").json()

