import rsa

from web_frame.context import private_key, public_key, config


def decrypt(content):
    if config.rsa:
        content = rsa.decrypt(content, private_key)
    return content


def encrypt(content):
    if config.rsa:
        content = rsa.encrypt(content, public_key)
    return content
