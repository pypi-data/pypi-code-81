import logging

from fastutils import dictutils
from fastutils import cipherutils
from fastutils import strutils

from django.db import models
from django.conf import settings
from django.db.models.lookups import IContains
from django.utils.datastructures import OrderedSet


logger = logging.getLogger(__name__)


class SafeFieldMixinBase(object):
    default_cipher_class = cipherutils.AesCipher
    default_result_encoder_class = {
        cipherutils.AesCipher: cipherutils.HexlifyEncoder,
        cipherutils.S12Cipher: cipherutils.HexlifyEncoder,
    }
    force_text_default = True
    text_encoding_default = "utf-8"
    default_kwargs = {
        cipherutils.AesCipher: {
            "key": cipherutils.mysql_aes_key,
        },
    }
    default_encrypt_kwargs = {}
    default_decrypt_kwargs = {}

    def get_cipher(self, **params):
        password = params.get("password", settings.SECRET_KEY)
        cipher_class = params.get("cipher_class", self.default_cipher_class)
        result_encoder = params.get("result_encoder", None)
        if not result_encoder:
            encoder_class = params.get("result_encoder_class", self.default_result_encoder_class.get(cipher_class, None))
            if encoder_class:
                result_encoder = encoder_class()
            else:
                result_encoder = None
        encrypt_kwargs = {}
        encrypt_kwargs.update(self.default_encrypt_kwargs.get(cipher_class, {}))
        encrypt_kwargs.update(params.get("encrypt_kwargs", {}))
        decrypt_kwargs = {}
        decrypt_kwargs.update(self.default_decrypt_kwargs.get(cipher_class, {}))
        decrypt_kwargs.update(params.get("decrypt_kwargs", {}))
        kwargs = {}
        kwargs.update(self.default_kwargs.get(cipher_class, {}))
        kwargs.update(params.get("kwargs", {}))
        force_text = params.get("force_text", self.force_text_default)
        text_encoding = params.get("text_encoding", self.text_encoding_default)
        cipher_params = dictutils.ignore_none_item({
            "password": password,
            "result_encoder": result_encoder,
            "kwargs": kwargs,
            "encrypt_kwargs": encrypt_kwargs,
            "decrypt_kwargs": decrypt_kwargs,
            "force_text": force_text,
            "text_encoding": text_encoding,
        })
        return cipher_class(**cipher_params)


    def __init__(self, *args, **kwargs):
        cipher_params = dictutils.ignore_none_item({
            "password": kwargs.pop("password", None),
            "result_encoder": kwargs.pop("result_encoder", None),
            "result_encoder_class": kwargs.pop("result_encoder_class", None),
            "cipher_class": kwargs.pop("cipher_class", None),
            "kwargs": kwargs.pop("kwargs", None),
            "encrypt_kwargs": kwargs.pop("encrypt_kwargs", None),
            "decrypt_kwargs": kwargs.pop("decrypt_kwargs", None),
            "force_text": kwargs.pop("force_text", None),
            "text_encoding": kwargs.pop("text_encoding", None),
            "encrypt_force_bytes": kwargs.pop("encrypt_force_bytes", None),
            "decrypt_force_bytes": kwargs.pop("decrypt_force_bytes", None),
        })
        self.cipher = kwargs.pop("cipher", self.get_cipher(**cipher_params))
        self.used_ciphers = []
        used_ciphers_params = kwargs.pop("used_ciphers", [])
        for used_cipher_params in used_ciphers_params:
            cipher = self.get_cipher(**used_cipher_params)
            self.used_ciphers.append(cipher)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        for cipher in [self.cipher] + self.used_ciphers:
            try:
                value = cipher.decrypt(value)
                return value
            except Exception:
                logger.warn("Warn: {0} has old cipher encrypted data.".format(self))
        logger.error("Error: SafeCharField.from_db_value decrypt failed: value={}".format(value))
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.cipher.encrypt(value)
        return strutils.force_text(value)

    def get_lookup(self, lookup_name):
        base_lookup = super().get_lookup(lookup_name)
        return type(base_lookup.__name__, (base_lookup,), {"get_db_prep_lookup": self.get_db_prep_lookup})

    def get_db_prep_lookup(self, value, connection):
        if callable(value):
            value = value()
        if isinstance(value, OrderedSet):
            value2 = OrderedSet()
            for item in value:
                value2.add(self.cipher.encrypt(item))
            value = value2
        else:
            value = [self.cipher.encrypt(value)]
        result = ('%s', value)
        return result

class SafeStringFieldMixin(SafeFieldMixinBase):
    pass

class SafeCharField(SafeStringFieldMixin, models.CharField):
    pass

class SafeTextField(SafeStringFieldMixin, models.TextField):
    pass

class SafeEmailField(SafeStringFieldMixin, models.EmailField):
    pass

class SafeURLField(SafeStringFieldMixin, models.URLField):
    pass

class SafeGenericIPAddressField(SafeStringFieldMixin, models.GenericIPAddressField):

    def __init__(self, *args, **kwargs):
        max_length = kwargs.pop("max_length", 128)
        super().__init__(*args, **kwargs)
        self.max_length = max_length

    def get_internal_type(self):
        return "CharField"


class SafeIntegerField(SafeFieldMixinBase, models.IntegerField):

    default_cipher_class = cipherutils.IvCipher
    force_text_default = False


class SafeNumbericFieldMixinBase(SafeFieldMixinBase):

    def force_numberic(self, value):
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        if isinstance(value, str):
            if "." in value:
                return float(value)
            else:
                return int(value)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.force_numberic(value)
        result = super().get_db_prep_value(value, connection, prepared)
        return result

class SafeBigIntegerField(SafeNumbericFieldMixinBase, models.CharField):

    def __init__(self, *args, **kwargs):
        cipher_kwargs = kwargs.pop("kwargs", {})
        cipher_kwargs["float_digits"] = 0
        kwargs["kwargs"] = cipher_kwargs
        kwargs["max_length"] = 128
        super().__init__(*args, **kwargs)

    default_cipher_class = cipherutils.IvfCipher
    force_text_default = False

class SafeFloatField(SafeNumbericFieldMixinBase, models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 128
        super().__init__(*args, **kwargs)

    default_cipher_class = cipherutils.IvfCipher
    force_text_default = False
