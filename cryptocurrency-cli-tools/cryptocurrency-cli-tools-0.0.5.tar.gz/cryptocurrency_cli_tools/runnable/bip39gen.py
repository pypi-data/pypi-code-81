#!/usr/bin/python3

# standard imports
import os
import sys
import logging
import argparse
import json

# third-party imports
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip32, EthAddr

logging.basicConfig()
logg = logging.getLogger()


argparser = argparse.ArgumentParser()
argparser.add_argument('-v', action='store_true', help='verbose logging')
argparser.add_argument('-n', type=int, default=10, help='number of addresses to derive')
argparser.add_argument('-p', action='store_true', default=False, help='include private keys in output')
argparser.add_argument('mnemonic', type=str, nargs='?', help='mnemonic')
args = argparser.parse_args()

if args.v:
    logg.setLevel(logging.DEBUG)

mnemonic = args.mnemonic
if mnemonic == None:
    mnemonic = os.environ.get('MNEMONIC')
if mnemonic == None:
    raise AttributeError('Mnemonic must be provided either as positional argument or environment variable MNEMONIC')
    sys.exit(1)

seed = Bip39SeedGenerator(mnemonic)
seed_bytes = seed.Generate()
logg.debug('seed {}'.format(seed_bytes))

b = Bip32.FromSeedAndPath(seed_bytes, "m/44'/60'/0'/0")
b = Bip44(b, Bip44Coins.ETHEREUM)

keys = {
        'public': [],
        'address': [],
    }
if args.p:
    keys['private'] = []


def main():
    for i in range(args.n):
        be = b.AddressIndex(i)
        pk = be.PrivateKey()
        pubk = be.PublicKey()

        pk_hex = pk.Raw().ToBytes().hex()
        logg.debug('pk {}'.format(pk_hex))

        pubk_hex = pubk.RawCompressed().ToBytes().hex()
        logg.debug('pubk {}'.format(pubk_hex))

        eth_address = pubk.ToAddress()
        logg.debug('addr {}'.format(eth_address))

        if args.p:
            keys['private'].append('0x' + pk_hex)
        keys['public'].append('0x' + pubk_hex)
        keys['address'].append(eth_address)

    sys.stdout.write(json.dumps(keys))


if __name__ == '__main__':
    main()
