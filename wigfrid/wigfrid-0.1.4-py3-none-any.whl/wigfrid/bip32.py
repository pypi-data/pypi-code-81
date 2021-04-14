import base64
from hashlib import blake2b
import hashlib
import hmac

from ecdsa import SigningKey, SECP256k1, VerifyingKey

from . import mnemonic

n = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141')
HIGHEST_BIT = 0x80000000;

# Refactored code segments from <https://github.com/keis/base58>
def b58encode(v: bytes) -> str:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    p, acc = 1, 0
    for c in reversed(v):
        acc += p * c
        p = p << 8

    string = ""
    while acc:
        acc, idx = divmod(acc, 58)
        string = alphabet[idx : idx + 1] + string
    return string

def b58decode(s):
    """ Decodes the base58-encoded string s into an integer """
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    base_count = len(alphabet)
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * alphabet.index(char)
        multi = multi * base_count
    return decoded

class ExtendKey:
    def __init__(self, privateKey: bytes):
        self.privateKey = privateKey
        self.publicKey = to_pub(privateKey)
        self.uncompressed_publickey = to_uncompressed(self.publicKey)
        self.address = to_addr(self.publicKey)

    @classmethod
    def from_mnemonic(cls, words):
        seed = mnemonic.to_seed(words)
        key_chain = key_derive_from_seed(seed)
        privkey = key_chain[:32]
        return ExtendKey(privkey)

def key_derive_from_seed(seed, path="m/44'/461'/0'/0/0"):
    seed = hmac.new(b"Bitcoin seed", seed, digestmod=hashlib.sha512).digest()
    li = path.split('/')[1:]
    for item in li:
        seed = derive(seed, item)
    return seed

def derive(seed: bytes, path: str):
    is_hardened = path[-1] == "'"
    # print('is_hardened %s' % is_hardened)
    master_key, chain_code = seed[:32], seed[32:]
    data = None
    if is_hardened:
        p = int(path[:-1]) + HIGHEST_BIT
        b = int.to_bytes(p, 4, 'big')
        data = b'\x00' + master_key + b
    else:
        p = int(path)
        b = int.to_bytes(p, 4, 'big')
        data = to_pub(master_key) + b
    seed = hmac.new(chain_code, data, digestmod=hashlib.sha512).digest()
        # return seed[:32] + b'\x00\x00' + seed[32:]
    IL = seed[:32]
    IR = seed[32:]
    key = (to_num(IL) + to_num(master_key)) %  to_num(n)
    key = to_bytes(key)
    return key + seed[32:]

def to_num(b):
    return int.from_bytes(b, 'big')

def to_bytes(n):
    return int.to_bytes(n, 32, 'big')

def to_pub(privkey: bytes):
    sk = SigningKey.from_string(privkey, curve=SECP256k1)
    vk = sk.verifying_key
    pubhex = vk.to_string().hex()
    end = int(pubhex[-1], 16)
    prefix = '02' if end % 2 == 0 else '03'
    return bytes.fromhex(prefix + pubhex[:64])

def to_uncompressed(pubkey: bytes):
    vk = VerifyingKey.from_string(pubkey, curve=SECP256k1)
    # return '04' + vk.to_string().hex()
    return b'\x04' + vk.to_string()

def get_payload(pubkey: bytes):
    h = blake2b(digest_size=20)
    h.update(pubkey)
    # h.hexdigest()
    return h.digest()

def get_checksum(payload: bytes):
    h = blake2b(digest_size=4)
    h.update(payload)
    return h.digest()

def sign(message_digest, privkey):
    sk = SigningKey.from_string(privkey, curve=SECP256k1)
    s = sk.sign_digest(message_digest)
    return s

def to_addr(pubkey: bytes):
    prefix = 'f1'
    payload = get_payload(to_uncompressed(pubkey))
    checksum = get_checksum(b'\x01' + payload)
    address = prefix + base64.b32encode(payload + checksum).decode().lower()
    return address[:41]
