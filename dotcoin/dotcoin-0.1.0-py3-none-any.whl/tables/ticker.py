from dotcoin.core.types import Table, Market, Ticker

_HEADER = "Last {base}/{quote}|Volume {base}|Var.|Bid {base}/{quote}|Ask {quote}/{base}"
_CONTENT = "{last}|{volume}|{var:.2f}%|{bid}|{ask}"


def _format_header(market: Market):
    header = _HEADER.format(**market.__dict__)
    return header.split("|")


def _format_content(ticker: Ticker):
    body = _CONTENT.format(**ticker.__dict__)
    return body.split("|")


def table_ticker(ticker: Ticker) -> Table:
    header = _format_header(ticker.context.market)
    content = _format_content(ticker)
    return Table(header, [content])
