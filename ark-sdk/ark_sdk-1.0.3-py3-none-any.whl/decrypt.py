import base64
import hashlib

from Crypto.Cipher import DES


def decrypt(password: str, val: str, repeat: int):
    if val is None:
        return val

    bytes_to_decrypt = base64.b64decode(val)
    md = hashlib.md5()
    md.update(password.encode('utf-8'))
    md.update(bytes_to_decrypt[:8])
    result = md.digest()
    for _ in range(1, repeat):
        md = hashlib.md5()
        md.update(result)
        result = md.digest()
    dec = DES.new(result[:8], DES.MODE_CBC, result[8:16])
    decrypted_text_bytes = dec.decrypt(bytes_to_decrypt[16:])
    decrypted_value = decrypted_text_bytes.rstrip(b'\2,\1,\3,\4,\5,\6,\7,\0').decode('utf-8')
    return decrypted_value.replace('\b', '')

