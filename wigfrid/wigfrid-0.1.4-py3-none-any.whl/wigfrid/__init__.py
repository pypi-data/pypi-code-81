import hashlib
from hashlib import blake2b
import base64
import json

from cbor2 import dumps, loads
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_string_canonize

from bip32 import ExtendKey

def to_bytes(value):
    if value == '0':
        return b''
    value = int(value)
    b = value.to_bytes((value.bit_length()+7) // 8 + 1, byteorder='big') 
    return b

def address_as_bytes(address):
    # print('address_as_bytes ', address)
    address_decoded = base64.b32decode(address[2:].upper() + '=')
    payload = address_decoded[:-4]
    return b'\x01' + payload

def transaction_serialize_raw(message):
    message =  {k.lower(): v for k, v in message.items()}  # lower keys
    to = address_as_bytes(message['to'])
    _from = address_as_bytes(message['from'])
    value = to_bytes(message['value'])
    gasfeecap = to_bytes(message['gasfeecap'])
    gaspremium = to_bytes(message['gaspremium'])
    message_to_encode = [
        0,
        to,
        _from,
        message['nonce'],
        value,
        message['gaslimit'],
        gasfeecap,
        gaspremium,
        message['method'],
        base64.b64encode(message['params'].encode()),
    ]
    data = dumps(message_to_encode)
    return data

CID_PREFIX = b'\x01\x71\xa0\xe4\x02\x20'

def cid(message):
    h = blake2b(digest_size=32)
    h.update(message)
    # h.hexdigest()
    return CID_PREFIX + h.digest()

def digest(unsigned_message):
    h = blake2b(digest_size=32)
    h.update(cid(unsigned_message))
    # h.hexdigest()
    return h.digest()


class Signature:
    def __init__(self, unsigned_message, private_key):
        serialized = transaction_serialize_raw(unsigned_message)
        message_digest = digest(serialized)
        privkey = base64.b64decode(private_key)
        sk = SigningKey.from_string(privkey, curve=SECP256k1)
        signature = sk.sign_digest_deterministic(message_digest, hashfunc=hashlib.sha256, sigencode=sigencode_string_canonize)
        self.data = base64.b64encode(signature + b'\x00').decode()  # 最后一个字节表示从签名中恢复公钥需要的次数, 在 secp256k1-node 中有体现
        # self.data = "D2PrURdLBSKvNzl4zr3Gvv1dAldvf+4EU1394sfZESsaKqxyYie4qeVFl7w4ZJ6rSO5cr1rvnpR+Q6muZTVTxAA="
        self.type = 1


class Message:
    def __init__(self, sm):
        self._from = sm['From']
        self.gaslimit = sm['GasLimit']
        self.gasfeecap = sm['GasFeecap']
        self.gaspremium = sm['GasPremium']
        self.method = sm['Method']
        self.nonce = sm['Nonce']
        self.params = sm['Params']
        self.to = sm['To']
        self.value = sm['Value']


class SignedMessage:
    def __init__(self, unsigned_message, private_key):
        # print('SignedMessage', sm)
        self.message = Message(unsigned_message)
        self.signature = Signature(unsigned_message, private_key)

def transaction_sign(unsigned_message, private_key):
    return SignedMessage(unsigned_message, private_key)

def transaction_sign_lotus(unsigned_message, private_key):
    signed_message = transaction_sign(unsigned_message, private_key);

    return json.dumps({
        'Message': {
            'From': signed_message.message._from,
            'GasLimit': signed_message.message.gaslimit,
            'GasFeeCap': signed_message.message.gasfeecap,
            'GasPremium': signed_message.message.gaspremium,
            'Method': signed_message.message.method,
            'Nonce': signed_message.message.nonce,
            'Params': signed_message.message.params,
            'To': signed_message.message.to,
            'Value': signed_message.message.value,
        },
        'Signature': {
            'Data': signed_message.signature.data,
            'Type': signed_message.signature.type,
        },
    })