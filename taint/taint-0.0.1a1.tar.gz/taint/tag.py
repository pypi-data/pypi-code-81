# standard imports
import hashlib
import logging

logg = logging.getLogger().getChild(__name__)


class TagPool:

    def __init__(self):
        self.tags = []
        self.tag_values = {}
        self.sum = b'\x00' * 32
        self.dirty = False
               

    def get(self):
        if self.dirty:
            self.tags.sort()
            h = hashlib.new('sha256') 
            for tag in self.tags:
                h.update(tag)
            self.sum = h.digest()
        return self.sum


    def add(self, tag, value=None):
        if tag in self.tags:
            return False
        self.tags.append(tag)
        self.tag_values[tag] = value
        self.dirty = True
        return True


    def create(self, value):
        h = hashlib.new('sha256')
        h.update(value)
        tag = h.digest()
        self.add(tag, value)
        return tag


    def merge(self, tags):
        if not isinstance(tags, TagPool):
            raise TypeError('tags must be type crypto_account_type.tag.TagPool')
        for tag in tags.tags:
            self.add(tag)
            self.tag_values[tag] = tags.tag_values[tag]

        for tag in self.tags:
            tags.add(tag)
            tags.tag_values[tag] = self.tag_values[tag]


    def serialize(self):
        b = self.get()
        for tag in self.tags:
            b += tag
        return b


    def deserialize(self, b):
        if len(b) % 32 > 0:
            raise ValueError('invalid data length; remainder {} from 32'.format(len(b) % 32))
        cursor = 32
        z = b[:cursor]

        for i in range(cursor, len(b), 32):
            tag = b[i:i+32]
            logg.debug('deserialize add {}'.format(tag))
            self.add(tag)

        zz = self.get()
        if z != zz:
            raise ValueError('data sum does not match content; expected {}, found {}'.format(zz.hex(), z.hex()))


    def __str__(self):
        tag_list = []
        for tag in self.tags:
            v = self.tag_values[tag]
            if v == None:
                v = tag.hex()
            else:
                try:
                    v = v.decode('utf-8')
                except UnicodeDecodeError:
                    v = v.hex()
            tag_list.append(v)
        tag_list.sort()
        return ','.join(tag_list)
