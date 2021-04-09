from dotcoin.core.types import Market, Order, Book, Table

_HEADER = "{quote}|{base}|PRICE|PRICE|{base}|{quote}"
_BID_ORDER = "{quote:>8f}|{base:>8f}|{price:>.8f}"
_ASK_ORDER = "{price:>8f}|{base:>8f}|{quote:>.8f}"


def _format_header(market: Market):
    header = _HEADER.format(**market.__dict__)
    return header.split("|")


def _format_order(bid: Order, ask: Order):
    bid_fmt = _BID_ORDER.format(**bid.__dict__)
    ask_fmt = _ASK_ORDER.format(**ask.__dict__)
    order_row = [*bid_fmt.split("|"), *ask_fmt.split("|")]
    return order_row


def _format_content(book: Book):
    zipped = zip(book.bids, book.asks)
    body = [_format_order(bid, ask) for bid, ask in zipped]
    return body


def table_book(book: Book) -> Table:
    header = _format_header(book.context.market)
    content = _format_content(book)
    return Table(header, content)
