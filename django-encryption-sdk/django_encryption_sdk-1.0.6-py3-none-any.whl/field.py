import django.dispatch
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from django_encryption.context import Context
from django_encryption.client import crypto_client

import logging

logger = logging.getLogger(__name__)
plain_sig = django.dispatch.Signal()


class DataKeeper(object):
    def __init__(self, plain_text=None, cipher_text=None, mask_type=None, field=None) -> None:
        self.plain_text = plain_text
        self.cipher_text = cipher_text
        self.model = field.model._meta.db_table
        self.field_name = field.column
        self.verbose_name = field.verbose_name
        self.mask_type = mask_type if mask_type is not None else ""
        self.id = None

    def plain(self):
        """
        获取原始明文，获取增加额外记录
        """
        try:
            plain_sig.send(sender=self.__class__, model=self.model, filed_name=self.field_name,
                           verbose_name=self.verbose_name, mask_text=self.mask(), cipher_text=self.cipher(), id=self.id,
                           context=Context.get())
        except Exception as e:
            logging.critical("send plain sig error, %s" % e, )

        if self.plain_text is not None:
            return self.plain_text

        return self.cipher_text if self.cipher_text is None else crypto_client().decrypt(self.cipher_text)

    def cipher(self):
        """
        获取密文
        """
        if self.cipher_text is not None:
            return self.cipher_text
        if self.plain_text is not None:
            self.cipher_text = crypto_client().encrypt(self.plain_text)
            return self.cipher_text
        return None

    def mask(self):
        """
        获取掩码信息
        """
        plain_info = self.plain_text if self.plain_text is not None else crypto_client().decrypt(self.cipher_text)

        if len(self.mask_type) <= 1:
            return "*"

        mask_type = self.mask_type.split("*")
        before = int(mask_type[0]) if mask_type[0].isdigit() else 0
        after = int(mask_type[-1]) if mask_type[-1].isdigit() else 0

        if len(plain_info) <= (before + after):
            return "***"

        mask_text = "***" if mask_type.count("*") > 1 else "*" * (len(plain_info) - before - after)
        return plain_info[:before] + mask_text + plain_info[len(plain_info) - after:]

    def __str__(self) -> str:
        return self.mask()

    def __repr__(self) -> str:
        return self.mask()


class DataKeeperCharField(CharField):
    description = _("Plain Data Keeper String (base CharField)")

    def __init__(self, mask_type="3**4", *args, **kwargs):
        """
        mask_type: [num1] (*|**) [num2]
        num1:前num1位明文显示
        (*|**): *表示固定三个*，(即***)，**表示按遮挡长度显示*
        num2: 后num2位明文显示
        """
        self.mask_type = mask_type
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """
        将会在从数据库中载入的生命周期中调用，包括聚集和 values() 调用
        """
        if value is None:
            return value
        return self.to_python(value)

    def to_python(self, value):
        """
        回显python
        """
        if value is None:
            return value

        if isinstance(value, DataKeeper):
            return value

        return DataKeeper(cipher_text=value, mask_type=self.mask_type, field=self)

    def get_prep_value(self, value):
        """
        落库
        """
        if value is None:
            return ""
        if isinstance(value, DataKeeper):
            return value.cipher()

        dk = DataKeeper(plain_text=value)
        return dk.cipher()

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Only include kwarg if it's not the default
        if self.mask_type != "3**4":
            kwargs["mask_type"] = self.mask_type
        return name, path, args, kwargs
