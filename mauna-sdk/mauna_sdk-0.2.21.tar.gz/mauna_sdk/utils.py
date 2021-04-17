import json
import secrets
import requests
from binascii import hexlify
from base64 import b64decode
from datetime import timezone, datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from . import config


IV = b"\x00" * 16


def _xor(b1, b2):
    longest, shortest = (b1, b2) if len(b1) >= len(b2) else (b2, b1)
    q, r = divmod(len(longest), len(shortest))
    result = bytearray()
    for a, b in zip(longest, shortest * q + shortest[:r]):
        result.append(a ^ b)
    return bytes(result)


def _now():
    """
    Return UTC timestamp
    """
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    return round(utc_time.timestamp())


def _gen_encryption_key(api_key, nonce):
    nonce_bytes = b64decode(nonce)
    api_key_bytes = bytes.fromhex(api_key)
    return _xor(api_key_bytes, nonce_bytes)


def _encrypt(data, key, iv):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()


def _decrypt(data, key, iv):
    unpadder = padding.PKCS7(128).unpadder()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dec_data = decryptor.update(data) + decryptor.finalize()
    unpadded_data = unpadder.update(dec_data) + unpadder.finalize()
    return unpadded_data.decode("utf-8")


def create_exchange_token(api_key, nonce_length=12):
    """
    Create exchange token
    """
    nonce = secrets.token_hex(round(nonce_length / 2))
    payload = {"timestamp": _now(), "nonce": nonce}
    return _encrypt(json.dumps(payload).encode(), bytes.fromhex(api_key), IV), nonce


def request_jwt(developer_id, token_payload):
    """
    Get the JWT given a developer ID and an exchange token
    """
    resp = requests.post(
        config.AUTH_ENDPOINT,
        data=json.dumps({"developer_id": developer_id, "token_payload": hexlify(token_payload).decode()}),
        headers={"Content-Type": "application/json"},
    )
    return resp.json()


def decrypt_jwt(auth_data, api_key, nonce):
    """
    Decrypt the JWT
    """
    enc_key = _gen_encryption_key(api_key, nonce)
    return _decrypt(bytes.fromhex(auth_data["enc_token"]), enc_key, IV)
