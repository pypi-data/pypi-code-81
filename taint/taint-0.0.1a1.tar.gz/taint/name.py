# standard imports
import hashlib


def for_label(chain_spec, label, salt):
    chain_str = str(chain_spec)
    h = hashlib.new('sha256')
    h.update(chain_str.encode('utf-8'))
    h.update(label)
    h.update(salt)
    z = h.digest()

    return z.hex()
