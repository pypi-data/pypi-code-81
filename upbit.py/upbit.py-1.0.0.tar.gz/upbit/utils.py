def markets_to_str(markets: list[str]) -> str:
    markets_str = str()
    for idx, market in enumerate(markets):
        markets_str += market
        if idx != len(markets) - 1:
            markets_str += ','
    return markets_str
