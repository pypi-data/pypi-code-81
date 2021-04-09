from bitcoinlib.wallets import Wallet
import bitcoinlib
import logging
from bitcoinlib.mnemonic import Mnemonic
from web3 import Web3

_logger = logging.getLogger(__name__)


class Wallet_Error(Exception):
    def __init__(self, msg):
        self.msg = msg
        _logger.error(msg)

    def __str__(self):
        return '지갑 이름에 유의하여주세요. 지갑 이름: %s' % self.msg


class Send_Error(Exception):
    def __init__(self, target):
        self.target = target
        _logger.error(target)

    def __str__(self):
        return '이체를 수행할 수 없습니다. \n' \
               '입금 지갑: %s \n' \
               '오류: 잔액이 부족하거나 입금 지갑 주소가 올바르지않습니다.' % self.target


class Btc(object):
    def __init__(self, name):
        self.name = name

    def create_wallet(self, network='bitcoin', passphrase=Mnemonic().generate()):
        try:
            w = Wallet.create(self.name, network=network, keys=passphrase)

            return w.get_key().address

        except bitcoinlib.wallets.WalletError:
            raise Wallet_Error(self.name)

    def wallet_scan(self):
        print(Wallet(self.name).scan())

    def wallet_info(self):
        print(Wallet(self.name).info())

    def btc_send(self, target=None, amount=None):
        try:
            t = Wallet(self.name).send_to(target, amount)
            print(t.info())

        except TypeError:
            print('주소와 수량 확인바랍니다.')
        except bitcoinlib.wallets.WalletError:
            raise Send_Error(target=target)
        except bitcoinlib.encoding.EncodingError:
            raise Wallet_Error(target)

    def get_balance(self):
        try:
            balance = Wallet(self.name).balance()

            return balance

        except bitcoinlib.wallets.WalletError:
            raise Wallet_Error


class Eth(object):
    def __init__(self, *kwargs):
        self.web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/b2862c602e244afa81a6b43d6d5a0a1a'))

    def create_wallet(self, name):
        n = self.web3.eth.account.create(name)

        return n._address

    def show_balance(self, address):
        balance = self.web3.eth.getBalance(address)

        return balance

    def send_trans(self, sender, receiver, amount):
        self.web3.eth.send_transaction({
              'from': sender,
              'to': receiver,
              'value': amount
        })