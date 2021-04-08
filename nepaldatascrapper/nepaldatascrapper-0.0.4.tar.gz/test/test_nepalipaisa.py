import pytest
import nepaldatascrapper
import datetime

nepse = nepaldatascrapper.NepaliPaisa()

def test_getData():
    data = nepse.getData()
    assert data != None
    print(data)

def test_dividend():
    data = nepse.getDividendInfo("2076/77")
    assert data != None
    print(data)

def test_investement():
    data = nepse.getInvestmentOpportunity()
    assert data != None
    print(data)

def test_agm():
    data = nepse.getAGMInfo("2076/77")
    assert data != None
    print(data)

def test_floorsheet():
    #data = nepse.getFloorSheet(datetime.datetime.today())
    data = nepse.getFloorSheet()
    assert data != None
    print(data)

