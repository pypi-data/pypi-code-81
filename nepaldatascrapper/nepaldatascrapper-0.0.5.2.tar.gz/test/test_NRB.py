import pytest
from nepaldatascrapper import NRB

def test_NRBExTable():
    nrb = NRB()
    table = nrb.NRBExTable()
    assert type(table) == type([])

def test_NRBExData():
    nrb = NRB()
    data = nrb.NRBExData("USD")
    assert type(data) == type(3.0)
