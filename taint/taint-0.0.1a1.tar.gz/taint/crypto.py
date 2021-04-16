# standard imports
import hashlib
import os

class Salter:

    salt = os.urandom(32)

    def __init__(self, chain_spec):
        self.chain_spec = chain_spec
        self.ionized_salt = self.salt
        self.ionized_salt = self.sprinkle(str(chain_spec).encode('utf-8'))


    def sprinkle(self, data):
        h = hashlib.new('sha256')
        if isinstance(data, list):
            for d in data:
                h.update(d)
        else:
            h.update(data)
        h.update(self.ionized_salt)
        return h.digest()

