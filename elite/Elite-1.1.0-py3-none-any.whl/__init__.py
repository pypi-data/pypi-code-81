'''
Elite - A package built for ECC security scheme.

This package contains high-level operations with the elliptic-curve
cryptography (ECC), as well as elliptic-curve diffie-hellman (ECDH)
key agreement protocol and elliptic-curve integrated encryption scheme
(ECIES) via cryptography providers.

This package also provides full encryption schemes, such as secp256k1
with AES_EAX for informal information transfer and secp384r1 with AES_GCM
for commercial and deep encryption.
'''

class EliteError(Exception):
    'General base class for errors.'

from . import cipher, secret, utils

# public apis
from .cipher import CryptoProvider, getprovider
from .scheme import ECCScheme, getscheme

# exceptions
from .cipher import EliteCryptoError, AuthorizationCodeInvalid
from .secret import EliteKeyError, UnsupportedCurve, CurveKindMismatch
from .scheme import EliteSchemeError, MissingRemoteKey
