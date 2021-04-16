# standard imports
import os
import logging

# external imports
from moolb import Bloom

# local imports
from .name import for_label
from .store import FileStore
from .account import Account

logg = logging.getLogger().getChild(__name__)


def to_index(block_height, tx_index):
    b = block_height.to_bytes(12, 'big')
    b += tx_index.to_bytes(4, 'big')
    return b


def from_index(b):
    block_height = int.from_bytes(b[:12], 'big')
    tx_index = int.from_bytes(b[12:], 'big')
    return (block_height, tx_index)


class CacheBloom:

    rounds = 3
    
    def __init__(self, bits_size):
        self.bits_size = bits_size
        self.filter = {
                'subject': None,
                'object': None,
                'cache': None,
                'extra': None,
                }


    def reset(self):
        self.filter['subject'] = Bloom(self.bits_size, CacheBloom.rounds)
        self.filter['object'] = Bloom(self.bits_size, CacheBloom.rounds)
        self.filter['cache'] = Bloom(self.bits_size, CacheBloom.rounds)
        self.filter['extra'] = Bloom(self.bits_size, CacheBloom.rounds)


    def add_raw(self, v, label):
        logg.debug('foo')
        self.filter[label].add(v)


    def serialize(self):
        if self.filter['subject'] == None:
            logg.warning('serialize called on uninitialized cache bloom')
            return b''

        b = self.filter['subject'].to_bytes() 
        b += self.filter['object'].to_bytes()
        b += self.filter['cache'].to_bytes()
        b += self.filter['extra'].to_bytes()
        return b


    def deserialize(self, b):
        byte_size = int(self.bits_size / 8)
        length_expect = byte_size * 4
        length_data = len(b)
        if length_data != length_expect:
            raise ValueError('data size mismatch; expected {}, got {}'.format(length_expect, length_data))

        cursor = 0
        self.filter['subject'] = Bloom(self.bits_size, CacheBloom.rounds, default_data=b[cursor:cursor+byte_size])

        cursor += byte_size
        self.filter['object'] = Bloom(self.bits_size, CacheBloom.rounds, default_data=b[cursor:cursor+byte_size])
    
        cursor += byte_size
        self.filter['cache'] = Bloom(self.bits_size, CacheBloom.rounds, default_data=b[cursor:cursor+byte_size])
        
        cursor += byte_size
        self.filter['extra'] = Bloom(self.bits_size, CacheBloom.rounds, default_data=b[cursor:cursor+byte_size])


    @staticmethod
    def from_serialized(b):
        if len(b) % 4 > 0:
            raise ValueError('invalid data length, remainder {} of 4'.format(len(b) % 32))

        bits_size = int((len(b) * 8) / 4)
        bloom = CacheBloom(bits_size)
        bloom.deserialize(b)
        return bloom


    def have(self, data, label):
        return self.filter[label].check(data)


    def have_index(self, block_height, tx_index):
        b = to_index(block_height, tx_index)
        if self.have(b, 'cache'):
            return True
        return self.have(b, 'extra')


    def register(self, accounts, block_height, tx_index):
        subject_match = False
        object_match = False
        for account in accounts:
            if self.have(account, 'subject'):
                subject_match = True
            elif self.have(account, 'object'):
                object_match = True

        if not subject_match and not object_match:
            return False

        b = to_index(block_height, tx_index)
        if subject_match:
            self.add_raw(b, 'cache')
        if object_match:
            self.add_raw(b, 'extra')

        return True


class Cache:

    def __init__(self, bits_size, store=None, cache_bloom=None):
        self.bits_size = bits_size
        self.store = store

        if cache_bloom == None:
            cache_bloom = CacheBloom(bits_size)
            cache_bloom.reset()

        self.cache_bloom = cache_bloom
        self.subjects = {}
        self.objects = {}

        self.first_block_height = -1
        self.first_tx_index = 0
        self.last_block_height = 0
        self.last_tx_index = 0


    def serialize(self):
        if self.first_block_height < 0:
            raise AttributeError('no content to serialize')

        b = to_index(self.first_block_height, self.first_tx_index)
        b += to_index(self.last_block_height, self.last_tx_index)
        bb = self.cache_bloom.serialize()
        return bb + b


    @staticmethod
    def from_serialized(b):
        cursor = len(b)-32
        bloom = CacheBloom.from_serialized(b[:cursor])
        c = Cache(bloom.bits_size, cache_bloom=bloom)

        (c.first_block_height, c.first_tx_index) = from_index(b[cursor:cursor+16])
        cursor += 16
        (c.last_block_height, c.last_tx_index) = from_index(b[cursor:cursor+16])

        return c


    def set_store(self, store):
        self.store = store
        if not store.initd and self.cache_bloom:
            self.store.save(self.cache_bloom.serialize())


    def divide(self, accounts):
        subjects = []
        objects = []

        for account in accounts:
            if self.cache_bloom.have(account, 'subject'):
                subject = self.subjects[account]
                subjects.append(subject)
            elif self.cache_bloom.have(account, 'object'):
                objct = self.objects[account]
                objects.append(objct)

        return (subjects, objects)


    def add_subject(self, account):
        if not isinstance(account, Account):
            raise TypeError('subject must be type crypto_account_cache.account.Account')
        self.cache_bloom.add_raw(account.account, 'subject')
        logg.debug('added subject {}'.format(account))
        self.subjects[account.account] = account


    def add_object(self, account):
        if not isinstance(account, Account):
            raise TypeError('subject must be type crypto_account_cache.account.Account')
        self.cache_bloom.add_raw(account.account, 'object')
        logg.debug('added object {}'.format(account))
        self.objects[account.account] = account


    def add_tx(self, sender, recipient, block_height, tx_index, relays=[]):
        accounts = [sender, recipient] + relays
        match =  self.cache_bloom.register(accounts, block_height, tx_index)

        if not match:
            return False

        if self.first_block_height == -1:
            self.first_block_height = block_height
            self.first_tx_index = tx_index
        self.last_block_height = block_height
        self.last_tx_index = tx_index

        logg.info('match in {}:{}'.format(block_height, tx_index))

        # TODO: watch out, this currently scales geometrically
        (subjects, objects) = self.divide(accounts)
        for subject in subjects:
            for objct in objects:
                subject.connect(objct) 
            for other_subject in subjects:
                if subject.is_same(other_subject):
                    continue
                subject.connect(other_subject)

        return True
       

    def have(self, block_height, tx_index):
        return self.cache_bloom.have_index(block_height, tx_index)
