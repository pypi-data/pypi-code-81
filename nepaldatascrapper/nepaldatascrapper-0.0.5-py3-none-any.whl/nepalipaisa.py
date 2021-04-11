from enum import Enum
import xmltodict
import requests
from .scrapper import Scrapper

class CategoryID(str, Enum):
    """
    Referes to various categoryID available for using with NepaliPaisa
    """
    AUCTION = "1"
    IPO = "2"
    FPO = "3"
    Right = "4"
    Mutual = "5"
    Debenture = "6"


class Index(str, Enum):
    """
    Referes to different NEPSE index available
    """
    Nepse = "Nepse"
    Banking = "Banking"
    DevBank = "Development Bank"
    Finance = "Finance"
    LifeInsurance = "Life Insurance"
    NonLifeInsurance = "Non Life Insurance"
    Hotels =  "Hotels"
    Hydropower = "HydroPower"
    Manufacture =  "Manu.& Pro."
    Trading = "Trading"
    Others =  "Others"
    Sensitive = "Sensitive"
    Float = "Float"
    SenFloat = "Sen. Float"

class NepaliPaisa(Scrapper):
    """
    class that fetches the data from nepalipaisa.com
    """

    def __init__(self):
        source = "http://www.nepalipaisa.com"
        endpoints = {
            "todayPrice":
            {
                "endpoint": "/Modules/GraphModule/webservices/MarketWatchService.asmx/GetTodaySharePrices",
                "parameter": {"fromdate": "", "toDate":"", "stockSymbol": "", "offset": 1, "limit": 50}
            },
            "dividend":
            {
                "endpoint": "/Modules/CompanyProfile//Webservices/CompanyService.asmx/GetAllDividendData",
                "parameter": {"offset":1, "limit":50, "FiscalYear":None, "SortBy":"BonusDistributionDate", "companyCode":None, "sectorName":""}
            },
            "investmentOpportunity":
            {
                "endpoint": "/Modules/Investment/webservices/InvestmentService.asmx/GetAllInvestmentInfobyCategoryID",
                "parameter": {"offset":1, "limit":50, "categoryID": CategoryID.IPO, "portalID":"1", "cultureCode":"en-US", "StockSymbol":None }
            },
            "agm":
            {
                "endpoint": "/Modules/AGM//Webservices/WebService.asmx/GetAGMList",
                "parameter": {"offset":1, "limit":50, "FiscalYear":"2076/77", "Sector":None, "StockName":None}
            },
            "floorsheet":
            {
                "endpoint": "/Modules/FloorSheet/WebService.asmx/GetFloorListView",
                "parameter": {"offset":1, "limit":100, "buyerID":None, "sellerID":None, "contractNo":"", "date":"08/05/2020", "stockSymbol":""}
            },
            "index":
            {
                "endpoint": "/Modules/Index/IndexView.asmx/GetAllIndices",
                "parameter": {"IndexName":"Nepse","IndexDateFrom":"2020-05-08","IndexDateTo":"2020-08-08"}
            }
        }
        super().__init__(source, endpoints)

    def post(self, endpoint, **kwargs):
        response = requests.post(self.getEndpoint(endpoint),params=kwargs)
        return response
    
    def getData(self, stockSymbol="", fromdate="", toDate="", offset=1, limit=50):
        """
        get stock data

        :param stockSymbol: nepse stock symbol
        :type stockSymbol: str
        :param fromdate: fetch data from this date
        :type fromdate: str
        :param toDate: fetch data to this date
        :type toDate: str
        :param offset: referes to offset
        :type offset: int
        :param limit: limit the result
        :type limit: int

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("todayPrice", stockSymbol=stockSymbol, fromdate=fromdate, toDate=toDate, offset=offset, limit=limit) 
        response = requests.post(self.getEndpoint("todayPrice"),params=postData);
        return xmltodict.parse(response.content)['ArrayOfTodaySharePrice']['TodaySharePrice']

    def getShareInfo(self, symbol, info, from_date="", to_date="", offset=1, limit=50):
        return self.getData(symbol, from_date, to_date, offset, limit)[info]

    def getSharePrice(self, symbol, from_date="", to_date="", offset=1, limit=50):
        return self.getData(symbol,from_date, to_date, offset, limit)["ClosingPrice"]
        #return [item["ClosingPrice"] for item in self.getData(symbol, from_date, to_date, offset, limit)]

    def getTodaysPrice(self):
        return self.getData()

    def getDividendInfo(self, fiscalYear=None, symbol=None ):
        """
        gets dividend information
        :param fiscalYear: fiscalYear in BS
        :type fiscalYear: str
        :param symbol: nepse stock symbol
        :type symbol: str

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("dividend", FiscalYear=fiscalYear, companyCode=symbol)
        response = self.post("dividend", **postData)
        return xmltodict.parse(response.content)
        #return response.json()['d']

    def getInvestmentOpportunity(self, categoryID = CategoryID.IPO, symbol=None):
        """
        gets investment opportunity

        :param categoryID: category 
        :type categoryID: CategoryID
        :param symbol: Nepse stock symbol
        :type symbol: str

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("investmentOpportunity", categoryID=categoryID, companyCode=symbol)
        response = self.post("investmentOpportunity", **postData)
        return xmltodict.parse(response.content)
        #return response.json()['d']

    def getAGMInfo(self, fiscalYear, symbol=None, sector=None):
        """
        gets agm information

        :param fiscalYear: fiscal year of which data is to be fetched 
        :type fiscalYear: str
        :param symbol: nepse stock symbol
        :type symbol str
        :param sector: filter as per sector

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("agm", fiscalYear=fiscalYear, StockName=symbol, Sector=sector)
        response = self.post("agm", **postData)
        return xmltodict.parse(response.content)
        #return response.json()['d']

    def getFloorSheet(self, date=""):
        """
        gets floorsheet:

        :param date: date
        :type date: str

        :returns: list of floorsheet
        :rtype: list
        """
        postData = self.createParameter("floorsheet", date=date)
        response = self.post("floorsheet", **postData)
