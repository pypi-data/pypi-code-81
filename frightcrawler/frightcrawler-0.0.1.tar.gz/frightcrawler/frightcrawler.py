#!/usr/bin/env python3

import argparse
import os
import time
import requests
import json
import csv
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'), help='Path to helvault.csv file')
    parser.add_argument(dest='format',
                        default='standard',
                        help='Choose the format',
                        nargs='?',
                        choices=['brawl','commander', 'duel', 'future', 'gladiator',
                        'historic', 'legacy', 'modern', 'oldschool', 'pauper', 'penny',
                        'pioneer', 'premodern', 'standard', 'vintage'])

    args = parser.parse_args()
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

    with args.file as helvaultdb:
        readHVDB = csv.reader(helvaultdb, delimiter=',')
        for row in readHVDB:
            scryID = 'https://api.scryfall.com/cards/' + row[6]
            scryAPI = requests.get(scryID)
            scryJSON = scryAPI.json()
            cardName = row[3]

            if args.brawl:
                cardStatus = dictor(scryJSON, 'legalities', search='brawl')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.commander:
                cardStatus = dictor(scryJSON, 'legalities', search='commander')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.duel:
                cardStatus = dictor(scryJSON, 'legalities', search='duel')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.future:
                cardStatus = dictor(scryJSON, 'legalities', search='future')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.gladiator:
                cardStatus = dictor(scryJSON, 'legalities', search='gladiator')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.historic:
                cardStatus = dictor(scryJSON, 'legalities', search='historic')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.legacy:
                cardStatus = dictor(scryJSON, 'legalities', search='legacy')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.modern:
                cardStatus = dictor(scryJSON, 'legalities', search='modern')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.oldschool:
                cardStatus = dictor(scryJSON, 'legalities', search='oldschool')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.pauper:
                cardStatus = dictor(scryJSON, 'legalities', search='pauper')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.penny:
                cardStatus = dictor(scryJSON, 'legalities', search='penny')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.pioneer:
                cardStatus = dictor(scryJSON, 'legalities', search='pioneer')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.premodern:
                cardStatus = dictor(scryJSON, 'legalities', search='premodern')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.standard:
                cardStatus = dictor(scryJSON, 'legalities', search='standard')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            if args.vintage:
                cardStatus = dictor(scryJSON, 'legalities', search='vintage')
                if cardStatus == ['legal']:
                    print('  ▓▒░░░    Legal    ', cardName)
                else:
                    print('  ▓▒░░░  Not legal  ', cardName)

            time.sleep(.1) #respect API rate limits

if __name__ == '__main__':
    main()
