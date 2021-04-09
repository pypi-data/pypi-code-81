from dotcoin.console.parser import main_parser
from dotcoin.console.actions import print_exchanges, print_markets, print_ticker, print_book


def main():
    args = main_parser()
    if args.cmd == 'exchanges':
        print_exchanges(args.span)
    elif args.cmd == 'markets':
        print_markets(args.span, args.compact)
    elif args.cmd == 'ticker':
        print_ticker(args.exchange, args.quote, args.base)
    elif args.cmd == 'book':
        print_book(args.exchange, args.quote, args.base)


__all__ = {'main'}
