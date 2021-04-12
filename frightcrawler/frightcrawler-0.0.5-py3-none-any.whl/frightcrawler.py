#!/usr/bin/env python3

import time
import argparse
import requests
import json
import csv
import sys
from dictor import dictor

intro = '''
  ▓░░░█▀▀░█▀▀▄░░▀░░█▀▀▀░█░░░░▀█▀░
  ▓░░░█▀░░█▄▄▀░░█▀░█░▀▄░█▀▀█░░█░░
  ▓░░░▀░░░▀░▀▀░▀▀▀░▀▀▀▀░▀░░▀░░▀░░
  ▓░█▀▄░█▀▀▄░█▀▀▄░█░░░█░█░░█▀▀░█▀▀▄
  ▓░█░░░█▄▄▀░█▄▄█░▀▄█▄▀░█░░█▀▀░█▄▄▀
  ▓░▀▀▀░▀░▀▀░▀░░▀░░▀░▀░░▀▀░▀▀▀░▀░▀▀
'''
print(intro)

class Logger(object):
    def flush(self):
        pass

    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("log.txt", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

sys.stdout = Logger()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'), help='path to csv file')
    parser.add_argument(dest='csv_file',
                        default='helvault',
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

    with args.file as cardlistCSV:
        cardlist = csv.reader(cardlistCSV, delimiter=',')
        next(cardlist)
        print('  Processing ' + args.csv_file +' CSV file for ' + args.format + ' format...\n')
        for row in cardlist:
            if args.helvault:
                scryID = 'https://api.scryfall.com/cards/' + row[6]
                cardName = row[3]

            if args.aetherhub:
                scryID = 'https://api.scryfall.com/cards/' + row[13]
                cardName = row[12]

            scryAPI = requests.get(scryID)
            scryJSON = scryAPI.json()

            if args.brawl:
                cardStatus = dictor(scryJSON, 'legalities', search='brawl', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.commander:
                cardStatus = dictor(scryJSON, 'legalities', search='commander', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.duel:
                cardStatus = dictor(scryJSON, 'legalities', search='duel', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.future:
                cardStatus = dictor(scryJSON, 'legalities', search='future', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.gladiator:
                cardStatus = dictor(scryJSON, 'legalities', search='gladiator', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.historic:
                cardStatus = dictor(scryJSON, 'legalities', search='historic', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.legacy:
                cardStatus = dictor(scryJSON, 'legalities', search='legacy', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.modern:
                cardStatus = dictor(scryJSON, 'legalities', search='modern', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.oldschool:
                cardStatus = dictor(scryJSON, 'legalities', search='oldschool', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.pauper:
                cardStatus = dictor(scryJSON, 'legalities', search='pauper', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.penny:
                cardStatus = dictor(scryJSON, 'legalities', search='penny', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.pioneer:
                cardStatus = dictor(scryJSON, 'legalities', search='pioneer', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.premodern:
                cardStatus = dictor(scryJSON, 'legalities', search='premodern', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.standard:
                cardStatus = dictor(scryJSON, 'legalities', search='standard', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.vintage:
                cardStatus = dictor(scryJSON, 'legalities', search='vintage', checknone=True)
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            time.sleep(.1) #respect API rate limits

if __name__ == '__main__':
    main()
