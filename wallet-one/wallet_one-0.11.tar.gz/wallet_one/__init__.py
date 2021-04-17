from typing import Dict
from collections import defaultdict
import binascii
from hashlib import md5, sha1

from enum import Enum


class TypeCrypt(Enum):
    """Types of crypts."""

    MD5 = 1
    SHA1 = 2


class Payment(object):
    """Wallet one payments."""

    def __init__(
        self,
        merchant_id: str,
        amount: float,
        secret: str,
        description: str,
        url_success: str,
        url_fail: str,
        currency: int = 643,
        override_fields: Dict = None,
        crypto_type: int = TypeCrypt.MD5.value,
    ):
        """Wallet one init."""
        self._secret = secret
        self._crypto_type = crypto_type
        self._form = {
            'WMI_MERCHANT_ID': merchant_id,
            'WMI_PAYMENT_AMOUNT': str(round(amount, 1)),
            'WMI_CURRENCY_ID': str(currency),
            'WMI_DESCRIPTION': description if description else 'Products',
            'WMI_SUCCESS_URL': url_success,
            'WMI_FAIL_URL': url_fail,
        }

        if override_fields and isinstance(override_fields, dict):
            self._form.update(override_fields)

    def _params(self) -> str:
        """Returns ordered form params as valued string."""
        params = [
            (pname, pval)
            for pname, pval in self._form.items()
            if pname != 'WMI_SIGNATURE'
        ]

        lcase = lambda s: str(s).lower()  # noqa

        lists_by_keys = defaultdict(list)
        for key, value in params:
            lists_by_keys[key].append(value)

        buffer = ''
        for key in sorted(lists_by_keys, key=lcase):
            for value in sorted(lists_by_keys[key], key=lcase):
                buffer += str(value)

        return buffer

    def _sign_data(self, raw_data: bytes) -> str:
        """Returns utf-decoded signature from form params as bytes."""
        eds = md5 if self._crypto_type == TypeCrypt.MD5.value else sha1
        base_view = binascii.b2a_base64(eds(raw_data).digest())[:-1]
        return base_view.decode('utf-8')

    @property
    def form(self) -> Dict:
        """Returns form data with signature for request."""
        form_data = dict(self._form)
        form_data.update({'WMI_SIGNATURE': self.signature})
        return form_data

    @property
    def signature(self) -> str:
        """Returns form signature for request."""
        params = f'{self._params().encode().decode("1251")}{self._secret}'
        return self._sign_data(params.encode())
