from argparse import Namespace, ArgumentParser


def main_parser() -> Namespace:
    parser = ArgumentParser(prog='parity')

    commands = parser.add_subparsers(dest='cmd')

    exchanges = commands.add_parser('exchanges', help='list supported exchanges')
    exchanges.add_argument('-s', '--span', type=int, default=3)

    markets = commands.add_parser('markets', help='list supported markets')
    markets.add_argument('-s', '--span', type=int, default=3)
    markets.add_argument('--compact', action='store_true')

    ticker = commands.add_parser('ticker', help='fetch ticker from a given market')
    ticker.add_argument('exchange', type=str)
    ticker.add_argument('quote', type=str)
    ticker.add_argument('base', type=str)

    book = commands.add_parser('book', help='fetch book from a given market')
    book.add_argument('exchange', type=str)
    book.add_argument('quote', type=str)
    book.add_argument('base', type=str)

    return parser.parse_args()
