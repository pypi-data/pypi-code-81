#!/usr/bin/env python3

import argparse
import csv
import sys
from time import sleep
from datetime import timedelta
from dictor import dictor
from requests_cache import CachedSession

INTRO = '''
  ▓░░░█▀▀░█▀▀▄░░▀░░█▀▀▀░█░░░░▀█▀░
  ▓░░░█▀░░█▄▄▀░░█▀░█░▀▄░█▀▀█░░█░░
  ▓░░░▀░░░▀░▀▀░▀▀▀░▀▀▀▀░▀░░▀░░▀░░
  ▓░█▀▄░█▀▀▄░█▀▀▄░█░░░█░█░░█▀▀░█▀▀▄
  ▓░█░░░█▄▄▀░█▄▄█░▀▄█▄▀░█░░█▀▀░█▄▄▀
  ▓░▀▀▀░▀░▀▀░▀░░▀░░▀░▀░░▀▀░▀▀▀░▀░▀▀
'''
print(INTRO)

class Logger:
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("frightcrawler-output.log", "a")

    def flush(self):
        pass

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

sys.stdout = Logger()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'), help='path to csv file')
    parser.add_argument(dest='csv_file',
                        help='set csv file layout',
                        choices=['helvault', 'aetherhub'])
    parser.add_argument(dest='format',
                        default='standard',
                        help='choose the format',
                        nargs='?',
                        choices=['brawl','commander', 'duel', 'future', 'gladiator',
                        'historic', 'legacy', 'modern', 'oldschool', 'pauper', 'penny',
                        'pioneer', 'premodern', 'standard', 'vintage'])

    args = parser.parse_args()
    args.helvault = (args.csv_file == 'helvault')
    args.aetherhub = (args.csv_file == 'aetherhub')
    args.brawl = (args.format == 'brawl')
    args.commander = (args.format == 'commander')
    args.duel = (args.format == 'duel')
    args.future = (args.format == 'future')
    args.gladiator = (args.format == 'gladiator')
    args.historic = (args.format == 'historic')
    args.legacy = (args.format == 'legacy')
    args.modern = (args.format == 'modern')
    args.oldschool = (args.format == 'oldschool')
    args.pauper = (args.format == 'pauper')
    args.penny = (args.format == 'penny')
    args.pioneer = (args.format == 'pioneer')
    args.premodern = (args.format == 'premodern')
    args.standard = (args.format == 'standard')
    args.vintage = (args.format == 'vintage')

    with args.file as cardlist_csv:
        cardlist = csv.reader(cardlist_csv, delimiter=',')
        next(cardlist)
        print('  Processing ' + args.csv_file +' CSV file for ' + args.format + ' format...\n')
        scry_cache = CachedSession(backend='sqlite',
                                   cache_name='scryfall-cache',
                                   expire_after=timedelta(days=3))
        for row in cardlist:
            if args.helvault:
                scry_id = 'https://api.scryfall.com/cards/' + row[6]
                card_name = row[3]
                foil_status = row[1]

            if args.aetherhub:
                scry_id = 'https://api.scryfall.com/cards/' + row[13]
                card_name = row[12]
                foil_status = row[7]

            if foil_status == '1' or foil_status == 'foil':
                foil = "◆"
            else:
                foil = '●'

            scry_api = scry_cache.request('GET', scry_id)
            scry_json = scry_api.json()

            if args.brawl:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.commander:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.duel:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.future:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.gladiator:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.historic:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.legacy:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.modern:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.oldschool:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.pauper:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.penny:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.pioneer:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.premodern:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.standard:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            if args.vintage:
                card_status = dictor(scry_json, 'legalities', search=args.format, checknone=True)
                set_name = dictor(scry_json, 'set_name')
                if card_status == ['legal']:
                    print('  ▓▒░░░    Legal   ', foil, card_name, '◄', set_name, '►')
                elif card_status == ['not_legal']:
                    print('  ▓▒░░░  Not legal ', foil, card_name, '◄', set_name, '►')

            sleep(.1) #respect API rate limits

if __name__ == '__main__':
    main()
