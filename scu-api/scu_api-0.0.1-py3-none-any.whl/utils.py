# -*- coding: utf-8 -*-

import hashlib
import base64

def password_encryption(password: str) -> str:
    hlmd5 = hashlib.md5()
    hlmd5.update(password.encode('utf-8'))
    return hlmd5.hexdigest()

def base64Img_encode(image: bytes) -> str:
    return str(base64.b64encode(image), 'utf-8')

def base64Img_decode(b64_image: str) -> bytes:
    return base64.b64decode(b64_image)
