from eth_account import (
    Account as EthAccount
)
from eth_account.messages import SignableMessage
from eth_account.datastructures import (
    SignedTransaction,
)
from eth_utils.curried import (
    hexstr_if_str,
    to_int,
    keccak,
)
from eth_keys import (
    # KeyAPI,
    keys,
)
from hexbytes import (
    HexBytes,
)
from collections.abc import (
    Mapping,
)
from cytoolz import (
    dissoc,
)
from conflux.address import Address
from conflux._utils.address import eth_address_to_cfx
from conflux._utils.signing import (
    sign_transaction_dict,
    to_standard_signature_bytes,
    to_standard_v,
)
from conflux._utils.transactions import (
    Transaction,
    vrs_from,
)

class Account:
    _keys = keys

    def __init__(self, account, network_id = None):
        self._inner_account = account
        self._network_id = network_id
        self._hex_address = eth_address_to_cfx(account.address)

    @property
    def hex_address(self):
        return self._hex_address

    @property
    def cfx_address(self):
        assert self._network_id is not None
        return Address.encode_hex_address(self._hex_address, self._network_id)

    @property
    def key(self):
        return self._inner_account.key

    @classmethod
    def create(cls, extra_entropy='', network_id = None):
        return Account(EthAccount.create(extra_entropy), network_id)

    @classmethod
    def from_key(cls, private_key, network_id = None):
        return Account(EthAccount.from_key(private_key), network_id)

    @classmethod
    def sign_message(cls, signable_message: SignableMessage, private_key):
        return EthAccount.sign_message(signable_message, private_key)

    @classmethod
    def recover_message(cls, signable_message: SignableMessage, vrs=None, signature=None):
        address = EthAccount.recover_message(signable_message, vrs, signature)
        return eth_address_to_cfx(address)

    @classmethod
    def sign_transaction(cls, transaction_dict, private_key):
        if not isinstance(transaction_dict, Mapping):
            raise TypeError("transaction_dict must be dict-like, got %r" % transaction_dict)

        account = EthAccount.from_key(private_key)

        # allow from field, *only* if it matches the private key
        if 'from' in transaction_dict:
            if Address.normalize_hex_address(transaction_dict['from']) == eth_address_to_cfx(account.address):
                sanitized_transaction = dissoc(transaction_dict, 'from')
            else:
                raise TypeError("from field must match key's %s, but it was %s" % (
                    eth_address_to_cfx(account.address),
                    transaction_dict['from'],
                ))
        else:
            sanitized_transaction = transaction_dict

        # sign transaction
        (
            v,
            r,
            s,
            rlp_encoded,
        ) = sign_transaction_dict(account._key_obj, sanitized_transaction)

        transaction_hash = keccak(rlp_encoded)

        return SignedTransaction(
            rawTransaction=HexBytes(rlp_encoded),
            hash=HexBytes(transaction_hash),
            r=r,
            s=s,
            v=v,
        )

    @classmethod
    def recover_transaction(cls, serialized_transaction):
        txn_bytes = HexBytes(serialized_transaction)
        txn = Transaction.from_bytes(txn_bytes)
        msg_hash = txn[0].hash()
        return cls._recover_hash(msg_hash, vrs=vrs_from(txn))

    @classmethod
    def _recover_hash(self, message_hash, vrs=None, signature=None):
        hash_bytes = HexBytes(message_hash)
        if len(hash_bytes) != 32:
            raise ValueError("The message hash must be exactly 32-bytes")
        if vrs is not None:
            v, r, s = map(hexstr_if_str(to_int), vrs)
            v_standard = to_standard_v(v)
            signature_obj = self._keys.Signature(vrs=(v_standard, r, s))
        elif signature is not None:
            signature_bytes = HexBytes(signature)
            signature_bytes_standard = to_standard_signature_bytes(signature_bytes)
            signature_obj = self._keys.Signature(signature_bytes=signature_bytes_standard)
        else:
            raise TypeError("You must supply the vrs tuple or the signature bytes")
        pubkey = signature_obj.recover_public_key_from_msg_hash(hash_bytes)
        return eth_address_to_cfx(pubkey.to_checksum_address())