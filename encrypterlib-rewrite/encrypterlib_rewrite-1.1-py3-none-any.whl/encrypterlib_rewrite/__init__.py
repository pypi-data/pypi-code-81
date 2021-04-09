version = "Release 1.0"
class asymmetric:
    from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey, _RSAPublicKey
    def generate_key(size: int = 4096):
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=size,
            backend=default_backend()
            )
    def generate_public_key(key: _RSAPrivateKey): return key.public_key()
    def generate_private_bytes_from_key(key: _RSAPrivateKey, password: bytes = None):
        from cryptography.hazmat.primitives import serialization
        return key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password) if type(password) == bytes else serialization.NoEncryption()
            )
    def generate_public_bytes_from_key(key: _RSAPublicKey):
        from cryptography.hazmat.primitives import serialization
        return key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
    def generate_key_from_private_bytes(private_bytes: bytes, password: bytes = None):
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        return serialization.load_pem_private_key(
            private_bytes,
            password=password if type(password) == bytes else None,
            backend=default_backend()
            )
    def generate_key_from_public_bytes(public_bytes: bytes):
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        return serialization.load_pem_public_key(
            public_bytes,
            backend=default_backend()
            )
    def decrypt(encrypted: bytes, private_key: _RSAPrivateKey):
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import hashes
        return private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
            )
    def encrypt(bytes: bytes, public_key: _RSAPublicKey):
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import hashes
        return public_key.encrypt(
            bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
            )
    #Code from https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/

class symmetric:
    def generate_random_key():
        from cryptography.fernet import Fernet
        return Fernet.generate_key()
    def _generate_key_from_password(password: bytes, salt: bytes = b"?i\xfbI\xce\x03\x16\x19\x92X\x19)\x1fA\x9e\xd3"):
        import base64
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))
    def generate_key_form_password(password: str, salt: bytes = b"?i\xfbI\xce\x03\x16\x19\x92X\x19)\x1fA\x9e\xd3"): _generate_key_from_password(password, salt)
    def _encrypt(bytes: bytes, key: bytes):
        from cryptography.fernet import Fernet
        return Fernet(key).encrypt(bytes)
    def encrypt(string: str, password: str): return symmetric._encrypt(string.encode(), symmetric.generate_key_from_password(password))
    def _decrypt(bytes: bytes, key: bytes):
        from cryptography.fernet import Fernet
        return Fernet(key).decrypt(bytes)
    def decrypt(encrypted_string: bytes, password: str): return symmetric._decrypt(encrypted_string, symmetric.generate_key_from_password(password)).decrypt()
    def generate_salt():
        import os
        return os.urandom(16)
    #Code from https://nitratine.net/blog/post/encryption-and-decryption-in-python/
