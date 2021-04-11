import nepaldatascrapper

def test_today_price():
    nepse = nepaldatascrapper.NepalStock()
    data = nepse.getSharePrice("NTC")
    assert len(data) > 0

