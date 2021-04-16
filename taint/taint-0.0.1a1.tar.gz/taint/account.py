# standard imports
import os

# local imports
from .tag import TagPool
from .crypto import Salter


class Account(Salter):

    def __init__(self, chain_spec, account, label=None, tags=[], create_digest=True):
        super(Account, self).__init__(chain_spec)

        if label == None:
            label = str(account)
        self.label = label
        self.account_src = None
        if create_digest:
            self.account_src = account
            self.account = self.sprinkle(self.account_src)
        else:
            self.account = account
        self.tags = TagPool()
        for tag in tags:
            self.tags.create(tag)


    def connect(self, account):
        if not isinstance(account, Account):
            raise TypeError('account must be type crypto_account_cache.account.Account')
        self.tags.merge(account.tags)


    def is_same(self, account):
        if not isinstance(account, Account):
            raise TypeError('account must be type crypto_account_cache.account.Account')
        return self.account == account.account


    def is_account(self, account):
        return self.sprinkle(account) == self.account


    def serialize(self):
        b = self.tags.serialize() + self.account
        return b


    @staticmethod
    def from_serialized(b, chain_spec, label=None):
        l = len(b)
        if l % 32 > 0:
            raise ValueError('invalid data length; remainder {} of 32'.format(l % 32))
        if l < 64: 
            raise ValueError('invalid data length; expected minimum 64, got {}'.format(l))

        a = Account(chain_spec, b[-32:], label=label, create_digest=False)
        a.tags.deserialize(b[:-32])
        return a


    def __str__(self):
        return '{} [{}]'.format(self.account.hex(), str(self.tags))
